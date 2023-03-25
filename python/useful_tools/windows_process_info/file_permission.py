"""


Created at 2023/3/8
"""
import win32api
import win32security
import ntsecuritycon as con

# 指定要修改权限的文件或目录
path = r"C:\path\to\file_or_folder"

# 获取当前用户的SID
username = win32api.GetUserName()
user_sid = win32security.LookupAccountName(None, username)[0]

# 获取文件或目录的句柄
handle = win32api.CreateFile(path, win32security.GENERIC_READ | win32security.WRITE_DAC, win32security.FILE_SHARE_READ | win32security.FILE_SHARE_WRITE, None, win32security.OPEN_EXISTING, win32security.FILE_FLAG_BACKUP_SEMANTICS, None)

# 获取文件或目录的安全描述符
sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)

# 创建只读访问控制项
ace = win32security.ACL()
ace.AddAccessAllowedAce(win32security.ACL_REVISION_DS, con.FILE_GENERIC_READ, user_sid)

# 将访问控制项添加到安全描述符的DACL中
dacl = sd.GetSecurityDescriptorDacl()
dacl.AddAce(win32security.ACL_REVISION_DS, con.FILE_GENERIC_READ, user_sid, True, False)
sd.SetSecurityDescriptorDacl(1, dacl, 0)

# 将新的安全描述符应用到文件或目录
win32security.SetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION, sd)

# 关闭文件或目录的句柄
win32api.CloseHandle(handle)
