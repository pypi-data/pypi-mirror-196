# LyCORIS - Lora beYond Conventional methods, Other Rank adaptation Implementations for Stable diffusion.

A project for implementing different algorithm to do parameter-efficient finetuning on stable diffusion or more.

This project is started from LoCon(see archive branch).


## What we have now
* Conventional LoRA
  * Include Conv layer implementation from LoCon


* LoRA with Hadamard Product representation (LoHa)
  * Ref: [FedPara Low-Rank Hadamard Product For Communication-Efficient Federated Learning](https://openreview.net/pdf?id=d71n4ftoCBy)
  * designed for federated learning, but has some cool property like rank<=dim^2 so should be good for parameter-efficient finetuning.
    * Conventional LoRA is rank<=dim


## usage
### For kohya script
Activate sd-scripts' venv and then install this package
```bash
source PATH_TO_SDSCRIPTS_VENV/Scripts/activate
```
or
```powershell
PATH_TO_SDSCRIPTS_VENV\Scripts\Activate.ps1 # or .bat for cmd
```

And then you can install this package:
* through pip
```bash
pip install lycoris
```

* from source
```bash
git clone https://github.com/KohakuBlueleaf/LyCORIS
cd LyCORIS
pip install .
```

Finally you can use this package's kohya module to run kohya's training script
```bash
python3 sd-scripts/train_network.py \
  --network_module lycoris.kohya \
  --network_dim "DIM_FOR_LINEAR" --network_alpha "ALPHA_FOR_LINEAR"\
  --network_args "conv_dim=DIM_FOR_CONV" "conv_alpha=ALPHA_FOR_CONV" \
  "dropout=DROPOUT_RATE" "algo=lora" \
```
to train lycoris module for SD model

* algo list:
  * lora: Conventional Methods
  * loha: Hadamard product representation introduced by FedPara

* Tips:
  * Use network_dim=0 or conv_dim=0 to disable linear/conv layer
  * LoHa doesn't support dropout yet.


### For a1111's sd-webui
download [Extension](https://github.com/KohakuBlueleaf/a1111-sd-webui-locon) into sd-webui, and then use your model as how you use lora model.
**LoHa Model supported**


### Additional Networks
Once you install the extension. You can also use your model in [addnet](https://github.com/kohya-ss/sd-webui-additional-networks/releases)<br>
just use it as LoRA model.
**LoHa Model not supported yet**


### Extract LoCon
You can extract LoCon from a dreambooth model with its base model.
```bash
python3 extract_locon.py <settings> <base_model> <db_model> <output>
```
Use --help to get more info
```
$ python3 extract_locon.py --help
usage: extract_locon.py [-h] [--is_v2] [--device DEVICE] [--mode MODE] [--safetensors] [--linear_dim LINEAR_DIM] [--conv_dim CONV_DIM]
                        [--linear_threshold LINEAR_THRESHOLD] [--conv_threshold CONV_THRESHOLD] [--linear_ratio LINEAR_RATIO] [--conv_ratio CONV_RATIO]
                        [--linear_percentile LINEAR_PERCENTILE] [--conv_percentile CONV_PERCENTILE]
                        base_model db_model output_name
```


## Example and Comparing for different algo
see [Demo.md](https://github.com/KohakuBlueleaf/LoCon/blob/lycoris/Demo.md) and [Algo.md](https://github.com/KohakuBlueleaf/LoCon/blob/lycoris/Algo.md)


## Todo list
- [ ] Module and Document for using LyCORIS in any other model, Not only SD.
- [ ] Proposition3 in [FedPara](https://arxiv.org/abs/2108.06098)
  * also need custom backward to save the vram
- [ ] Low rank + sparse representation
- [ ] Support more operation, not only linear and conv2d.
- [ ] Configure varying ranks or dimensions for specific modules as needed.
- [ ] Automatically selecting an algorithm based on the specific rank requirement.
- [ ] Explore other low-rank representations or parameter-efficient methods to fine-tune either the entire model or specific parts of it.
- [ ] More experiments for different task, not only diffusion models.


## Citation
```bibtex
@misc{LyCORIS,
  author       = "Shih-Ying Yeh (Kohaku-BlueLeaf)",
  title        = "LyCORIS - Lora beYond Conventional methods, Other Rank adaptation Implementations for Stable diffusion",
  howpublished = "\url{https://github.com/KohakuBlueleaf/LyCORIS}",
  month        = "Feb",
  year         = "2023"
}
```