#!/bin/bash

# Specify the directory structure and layer package name
LAYER_DIR="python"
LAYER_PACKAGE="libraries_layer_package.zip"

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check if the requirements.txt file exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found!"
    exit 1
fi

# Remove previous layer directory and zip if they exist
rm -rf $LAYER_DIR
rm -f $LAYER_PACKAGE

# Install Python packages specified in requirements.txt
pip install -r requirements.txt -t $LAYER_DIR/

# Zip the layer
zip -r $LAYER_PACKAGE $LAYER_DIR

# Provide feedback on where the layer was saved
echo "Layer packaged as $LAYER_PACKAGE"