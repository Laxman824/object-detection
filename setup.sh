4. Create `setup.sh` script:
```bash
#!/bin/bash

# Create required directories
mkdir -p tmp/model/rfcn/1

# Download and extract model if not exists
if [ ! -f tmp/model/rfcn/1/saved_model.pb ]; then
    echo "Downloading RFCN model..."
    wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
    tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
    mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/rfcn/1/
    rm -rf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz tmp/rfcn_resnet101_coco_2018_01_28
fi

# Make script executable
chmod +x setup.sh