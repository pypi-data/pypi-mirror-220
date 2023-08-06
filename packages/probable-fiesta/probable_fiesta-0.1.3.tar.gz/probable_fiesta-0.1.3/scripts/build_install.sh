#!/bin/bash
# Dinamically build and install latest pip version.

# Package variables
package_name="probable-fiesta"
package_src="probable_fiesta"
package_dist_src="probable_fiesta"

# Get current directory parent dir
dir="$(pwd)"
parentdir="$(dirname "$dir")"

# Parse file containing version
file=${parentdir}/${package_name}/src/${package_src}/__about__.py
name=$(<"$file")       #the output of 'cat $file' is assigned to the $name variable
version=$(echo $name | cut -d \' -f2)

# Build package
hatch build

# Install package
pip install -U dist/${package_dist_src}-${version}.tar.gz
