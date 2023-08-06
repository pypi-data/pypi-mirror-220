import re
import warnings
import subprocess

from groundingdino.version import __version__, __torch_version__, __torchvision_version__, force_install


class CheckInstalled:
    def __init__(self, force_install):
        self.force_install = force_install
        self.stk_version = __version__

        self.names = ['nvcc', 'nvcc_digits', 'nvcc_dino_digits',
                      'req_torch', 'req_torchvision',
                      'req_torch_digits', 'req_torchvision_digits',
                      'curr_torch', 'curr_torchvision',
                      'curr_torch_str', 'curr_torchvision_str',
                      'curr_torch_digits', 'curr_torchvision_digits'
                      ]

        self.__versions = {x: None for x in self.names}

        # Ex:
        # 1.0.0.2.0.118
        # {1.0.0}.{2.0}.{118}
        # <groundingdino_stk_version>.<torch_version>.<nvcc_version>
        self.__versions['nvcc_dino_digits'] = self.stk_version.split('.')[5]

        self.__versions['req_torch'] = __torch_version__
        self.__versions['req_torchvision'] = __torchvision_version__


    def __get_nvcc__(self) -> None:
        try:
            output = subprocess.check_output(
                ["nvcc", "-V"], stderr=subprocess.STDOUT
                ).decode("utf-8")

            version_match = re.search(r"release (\d+\.\d+)", output)
            if version_match:
                self.__versions['nvcc'] = version_match.group(1)
            else:
                print("Failed to extract nvcc version")
        except subprocess.CalledProcessError as e:
            print(f"Error executing nvcc command: {e.output.decode('utf-8')}")


        if self.__versions['nvcc'] is not None:
            if int(self.__versions['nvcc'].split('.')[0]) >= 12:
                self.__versions['nvcc'] = '11.8'

            self.__versions['nvcc_digits'] = self.__versions['nvcc'] \
                                                 .replace('.', '')

    def __get_pip__(self) -> None:

        try:
            output = subprocess.check_output(
                ["pip3", "freeze"], stderr=subprocess.STDOUT).decode()

            for line in output.split('\n'):
                line = line.strip()

                if 'torch' not in line and 'torchvision' not in line:
                    continue

                line_text = re.split(r'==|@', line)[0].strip()

                if line_text not in ['torch', 'torchvision']:
                    continue

                if '==' in line:
                    line_str = line
                elif '@' in line:
                    if line_text == 'torch':
                        from torch import __version__ as __curr_torch_version__
                        line_str = f"{line_text}=={__curr_torch_version__}"
                    elif line_text == 'torchvision':
                        from torchvision import __version__ as __curr_torchvision_version__
                        line_str = f"{line_text}=={__curr_torchvision_version__}"

                self.__versions[f"curr_{line_text}_str"] = line_str

                if self.__versions['curr_torch_str'] is not None and self.__versions['curr_torchvision_str'] is not None:
                    break

        except Exception as ex:
            print(ex)

        if self.__versions['curr_torch_str'] is not None:
            self.__versions['curr_torch'] = self.__versions['curr_torch_str'] \
                                                .split('==')[-1] \
                                                .split('+')[0]

        if self.__versions['curr_torchvision_str'] is not None:
            self.__versions['curr_torchvision'] = self.__versions['curr_torchvision_str'] \
                .split('==')[-1] \
                .split('+')[0]

    def __using_cpu__(self) -> bool:
        return '+cu' not in self.__versions['curr_torch_str'] or '+cu' not in self.__versions['curr_torchvision_str']
    
    def __dino_cuda_is_match__(self) -> bool:
        return self.__versions['nvcc_dino_digits'] == self.__versions['nvcc_digits']

    def __cuda_is_match__(self) -> bool:
        return self.__versions['nvcc_digits'] == self.__versions['curr_torch_str'].split('+cu')[-1] and \
            self.__versions['nvcc_digits'] == self.__versions['curr_torchvision_str'].split('+cu')[-1]

    def __install__(self) -> None:
        if self.force_install:
            package_name = " ".join(f"{k}~={v}" for k, v in zip(['torch', 'torchvision'],
                                                                [self.__versions['req_torch'], self.__versions['req_torchvision']])
                                    )
            install_command = f'pip3 install {package_name} ' + \
                f'--index-url https://download.pytorch.org/whl/cu{self.__versions["nvcc_digits"]} ' + \
                f'--force-reinstall'

            try:
                print('Installing package')
                subprocess.check_call(install_command.split())
                print(f"Successfully installed {package_name}")

            except subprocess.CalledProcessError:
                print(f"Failed to install {package_name}")

    def __get_digit_version__(self, version: str, round: int) -> str:
        return '.'.join(version.split('.')[:round])

    def __is_installed__(self) -> None:
        self.__versions['req_torch_digits'] = self.__get_digit_version__(
            self.__versions['req_torch'], 2)
        self.__versions['req_torchvision_digits'] = self.__get_digit_version__(
            self.__versions['req_torchvision'], 2)

        self.__versions['curr_torch_digits'] = self.__get_digit_version__(
            self.__versions['curr_torch'], 2)
        self.__versions['curr_torchvision_digits'] = self.__get_digit_version__(
            self.__versions['curr_torchvision'], 2)

        return self.__versions['curr_torch_digits'] == self.__versions['req_torch_digits'] and \
            self.__versions['curr_torchvision_digits'] == self.__versions['req_torchvision_digits']

    def run(self) -> None:
        self.__get_nvcc__()

        if self.__versions['nvcc'] is None:
            warnings.warn("Nvcc is not installed", stacklevel=2)

        elif not self.__dino_cuda_is_match__():
            warnings.warn("The Cuda of groundingdino version is not matched with nvcc", stacklevel=2)
            warnings.warn("Please remove groundingdino and install correspondingly version again.", stacklevel=2)

        else:
            self.__get_pip__()

            # torch or torchvision are not installed or using cpu.
            if self.__versions['curr_torch_str'] is None \
                    or self.__versions['curr_torchvision_str'] is None \
                    or self.__using_cpu__() \
                    or not self.__cuda_is_match__() \
                    or not self.__is_installed__():
                self.__install__()

        
app = CheckInstalled(force_install)
app.run()
