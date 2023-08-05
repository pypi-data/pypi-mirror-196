from tayto import linux


def pushcode(src:str, dst:str, base:str, new:str) -> None:
  from uuid import uuid4
  folder = f'/tmp/{uuid4()}'
  linux.bash(f'''
rm -rf {folder}
mkdir -p {folder}/code
cd {folder}
ln -s {src} code
cat > Dockerfile << EOF
FROM {base}
ADD code {dst}
EOF
docker image rm -f {new}
docker build -t {new} .
cd ~
''')

