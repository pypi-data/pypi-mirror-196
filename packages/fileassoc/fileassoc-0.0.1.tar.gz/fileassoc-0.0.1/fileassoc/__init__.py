import winreg

def execute(extension, appPath):
        extension = r'Software\Classes\.' + extension
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, extension)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, appPath)
        cmd_key = winreg.CreateKey(key, 'shell\\open\\command')
        winreg.SetValueEx(cmd_key, '', 0, winreg.REG_SZ, f'"{appPath}" "%1"')
        winreg.CloseKey(key)