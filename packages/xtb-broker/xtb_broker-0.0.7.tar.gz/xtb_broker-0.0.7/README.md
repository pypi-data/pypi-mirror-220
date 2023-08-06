# Update build
> python3 -m pip install --upgrade build

# Generating distribution archives
Now run this command from the same directory where pyproject.toml is located to generate dist
> python setup.py sdist bdist_wheel

# Install twine
> python3 -m pip install --upgrade twine

# Uploading the distribution archives 
> twine upload dist/*

# include version in requirements 
> xtb-broker==0.0.1 

# pip install
> pip install xtb-broker==0.0.1
> 
> 

