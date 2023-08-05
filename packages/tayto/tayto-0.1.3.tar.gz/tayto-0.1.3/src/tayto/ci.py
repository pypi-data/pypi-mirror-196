from tayto import linux


def pushcode(src:str, dst:str, base:str, new:str) -> None:
  linux.bash(f'''
cd {src}
cat > Dockerfile << EOF
FROM {base}
ADD build {dst}
EOF
docker build -t {new} .
cd ~
''')

