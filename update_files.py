import paramiko


host = '46.173.223.53'
user = 'root'
password = 'auf4len228'
port = 22

transport = paramiko.Transport((host, port))
transport.connect(username=user, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

local_path = './dir.zip'
remote_path = './dir.zip'

sftp.put(local_path, remote_path)

# Обновить папки
# destination_dir = './Kyve'
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(hostname=host, username=user, password=password)
# channel = client.get_transport().open_session()
# channel.exec_command(f'rm -rf {destination_dir} && unzip {remote_path} -d {destination_dir}')
# while not channel.exit_status_ready():
#     pass
# channel.close()
# sftp.remove(remote_path)

sftp.close()
transport.close()