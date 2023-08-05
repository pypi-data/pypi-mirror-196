
<h1 align="center">
  <br>
  <a href="https://rafsunsheikh.github.io/Web"><img src="https://raw.githubusercontent.com/rafsunsheikh/ptmodels/master/image_sources/logo_hi.png" alt="ptmodels" width="200"></a>
  <br>
  ptmodels
  <br>
</h1>

<h4 align="center">ptmodels uses pre-trained models to evaluate image datasets and helps to understand which model works better.<a href="https://pypi.org/project/ptmodels/" target="_blank">ptmodels</a>.</h4>

<p align="center">
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">
  </a>
  <a href="https://www.paypal.me/AmitMerchant">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#table-of-content">Table-of-Contents</a> •
  <a href="#installation">Installation</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#classification">Classification</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

![screenshot](https://raw.githubusercontent.com/rafsunsheikh/ptmodels/master/image_sources/evaluation_01.png)


## Table of Contents

- [Installation](##installation)
    - [Stable Release](###stable-release)
    - [From Sources](###from-sources)
- [How to Use](##How-to-use)
    - [Preprocessing](##preprocessing) 
        - [Import Library](###import)
        - [PreTrainedModels Class](###pretrainedmodels-class)
        - [Available Models](###available-models)
        - [Load Dataset](###load-dataset)
        - [load_models() Method](###load-models-method)
        - [models_name() Method](###models-name-method)
    - [Classification](##classification)
        - [fit() Method](###fit-method)  
        - [train_specific_model() Method](###train-specific-model-method)
    - [Evaluation](##evaluation)
        - [evaluate_saved_model() Method](###evaluate-saved-model-method)
        - [predict_image_saved_model() Method](###predict-image-saved-model-method)
- [Credits](##credits)
- [Related](##related)
- [Support](##support)
- [You May Also Like](##you-may-also-like)
- [License](##license)



## Why must you document your project? <a name = "why_document"></a>

## Installation <a name = "installation"></a>

### Stable Release <a name = "stable-release"></a>
* Install ptmodels by using `pip install` into the terminal
```bash
pip install ptmodels
```

### From Sources <a name = "from-sources"></a>
- To install a Python package from a source other than the PyPI repository, you can download and unpack the source distribution yourself, and then use its `setup.py` script to install the package in the user `site-packages` directory:
- Set up your user environment
- Use the `wget` command to download the distribution archive (for example, 0.1.0.tar.gz) from the source (for example, https://github.com/rafsunsheikh/ptmodels/archive/refs/tags/0.1.0.tar.gz); for example:
```
wget https://github.com/rafsunsheikh/ptmodels/archive/refs/tags/0.1.0.tar.gz
```
- Use `tar` to unpack the archive. For example:
```
tar ptmodels-0.1.0.tar.gz
```
The distribution should unpack into a similarly-named directory in your home directory (for example, ~/ptmodels-0.1.0).
- Change (`cd`) to the new directory, and then, on the command line, enter:
```
python setup.py install --user
```
The `--user` option directs `setup.py` to install the package (for example, ptmodels) in the user `site-packages` directory for the running Python; for example:
```
~/.local/lib/pythonX.Y/site-packages/ptmodels
```
Python automatically searches this directory for modules, so prepending this path to the PYTHONPATH environmental variable is not necessary.

If you omit the `--user` option, `setup.py` will try to install the package in the global `site-packages` directory (where you do not have the necessary permissions); as a result, the installation will fail.

Alternatively, you can use the `--home` or `--prefix` option to install your package in a different location (where you have the necessary permissions); for example, to install your package in a subdirectory (for example, python-pkgs):
- Within your home directory, enter:
```
python setup.py install --home=~/python-pkgs
```


## How To Use <a name = "how-to-use"></a>

## Preprocessing <a name = "preprocessing"></a>
- Open up Kaggle Notebook or Google Colab.
- Choose runtime with GPU support. (as the models are very large, it will be difficult to run it on your local machine and also without GPU.)
- Install ptmodels in one cell.
```
!pip install ptmodels
```
- Run the cell by pressing shift + enter

### Import Library <a name = "import-library"></a>
Import `PreTrainedModels` class from `ptmodels.Classifier` package. 
```bash
from ptmodels.Classifier import PreTrainedModels
```
### PreTrainedModels Class <a name = "pretrainedmodels-class"></a>
- PreTrainedModels class is the only class of this package. It's an easy-to-use class with some parameters. You can call the PreTrainedModels class without any arguments. That time default values will be set in the parametes. Or else you can provide your own arguments values.
#### Arguments
- **NUM_CLASSES** : Takes the number of classes for classification. Default value is set to **2**.
- **BATCH_SIZE** : Trains the image dataset into batches. Defaults Batch size value is **32**.
- **EPOCHS** : Takes the number of number of epochs for the training. Default value set to **1**.
- **LEARNING_RATE** : Sets the learning rate for training the model. Default value set to **1e-4**. 
- **MOMENTUM** : Sets the value of momentum for training the model. Default value set to **0.9**.

#### Example
```
model = PreTrainedModels(NUM_CLASSES=10, BATCH_SIZE=32, EPOCHS=1, LEARNING_RATE=0.001, MOMENTUM=0.9)
```

- You can also consuly my [Google Colab Notebook](https://colab.research.google.com/drive/19BJ0LAQrqTEZiMqRAXZDZH5dhgwQeRI_?usp=sharing)

### Available Models <a name = "available-models"></a>
Following are the available models for `ptmodels` package:

| Model	| Size (MB) | Top-1 Accuracy |	Top-5 Accuracy | Parameters	| Depth |	Time (ms) per inference step (CPU) | Time (ms) per inference step (GPU) |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
|VGG16 | 528 | 71.3% |	90.1% | 138.4M | 16	| 69.5	| 4.2 |
|VGG19 |	549 |	71.3% |	90.0% |	143.7M |	19 |	84.8 |	4.4 |
|ResNet50 |	98 |	74.9% |	92.1% |	25.6M |	107 |	58.2 |	4.6 |
|ResNet50V2 |	98 |	76.0% |	93.0% |	25.6M |	103 |	45.6 |	4.4 |
|ResNet101 |	171 |	76.4% |	92.8% |	44.7M |	209 |	89.6 |	5.2 |
|ResNet101V2 |	171 |	77.2% |	93.8% |	44.7M |	205 |	72.7 |	5.4 |
|ResNet152 |	232 |	76.6% |	93.1% |	60.4M |	311 |	127.4 |	6.5 |
|ResNet152V2 |	232 |	78.0% |	94.2% |	60.4M |	307 |	107.5 |	6.6 |
|MobileNet |	16	| 70.4% |	89.5% |	4.3M |	55 |	22.6 |	3.4 |
|MobileNetV2 |	14 |	71.3% |	90.1% |	3.5M |	105 |	25.9 |	3.8 |
|DenseNet121 |	33 |	75.0% |	92.3% |	8.1M |	242 |	77.1 |	5.4 |
|DenseNet169 |	57 |	76.2% |	93.2% |	14.3M |	338 |	96.4 |	6.3 |
|DenseNet201 |	80 |	77.3% |	93.6% |	20.2M |	402 |	127.2 |	6.7 |
|NASNetMobile |	23 |	74.4% |	91.9% |	5.3M |	389 |	27.0 |	6.7 |
|NASNetLarge |	343 |	82.5% |	96.0% |	88.9M |	533 |	344.5 |	20.0 |
|EfficientNetB0 |	29 |	77.1% |	93.3% |	5.3M |	132 |	46.0 |	4.9 |
|EfficientNetB1 |	31 |	79.1% |	94.4% |	7.9M |	186 |	60.2 |	5.6 |
|EfficientNetB2 |	36 |	80.1% |	94.9% |	9.2M |	186 |	80.8 |	6.5 |
|EfficientNetB3 |	48 |	81.6% |	95.7% |	12.3M |	210 |	140.0 |	8.8 |
|EfficientNetB4 |	75 |	82.9% |	96.4% |	19.5M |	258 |	308.3 |	15.1 |
|EfficientNetB5 |	118 |	83.6% |	96.7% |	30.6M |	312 |	579.2 |	25.3 |
|EfficientNetB6 |	166 |	84.0% |	96.8% |	43.3M |	360 |	958.1 |	40.4 |
|EfficientNetB7 |	256 |	84.3% |	97.0% |	66.7M |	438 |	1578.9	| 61.6 |
|EfficientNetV2B0 |	29 |	78.7% |	94.3% |	7.2M |	- |	- |	- |
|EfficientNetV2B1 |	34 |	79.8% |	95.0% |	8.2M |	- |	- |	- |
|EfficientNetV2B2 |	42 |	80.5% |	95.1% |	10.2M |	- |	- |	- |
|EfficientNetV2B3 |	59 |	82.0% |	95.8% |	14.5M |	- |	- |	- |
|EfficientNetV2S |	88 |	83.9% |	96.7% |	21.6M |	- |	- |	- |
|EfficientNetV2M |	220 |	85.3% |	97.4% |	54.4M |	- |	- |	- |
|EfficientNetV2L |	479 |	85.7% |	97.5% |	119.0M | - | - | - |
|ConvNeXtTiny |	109.42 |	81.3% |	- |	28.6M	| - |	- |	- |
|ConvNeXtSmall |	192.29 |	82.3% |	- |	50.2M	| - |	- |	- |
|ConvNeXtBase |	338.58 |	85.3% |	- |	88.5M	| - |	- |	- |
|ConvNeXtLarge |	755.07 |	86.3% |	- |	197.7M	| - |	- |	- |
|ConvNeXtXLarge |	1310 |	86.7% |	- |	350.1M | - |	- |	- |

- All these models are taken from Keras Application API. These models are used as image classification using pre-trained weights. Prediction, feature extraction, and fine-tuning can be done using these models.

### Load Dataset <a name = "load-dataset"></a>

- You can use any image dataset available online or use your own image dataset.
-  Load your dataset in the preffered way. 
-  For this documentation we have used `Cifar10` image dataset that is freely available in the `keras.datasets`. 
-  This dataset has 50,000 32x32 colored training images and 10,000  colored test images. There are 10 categories in this dataset. See more info at the <a href="https://www.cs.toronto.edu/~kriz/cifar.html">CIFAR homepage</a>. 


#### Example: 
- We are getting the dataset from `tensorflow.keras.datasets`.
- You can get your own dataset from anywhere. 
```
from tensorflow.keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
```
- After loading the dataset please split the dataset into `(x_train, y_train), (x_test, y_test)`.
- For that you can use `sklearn.model_selection.train_test_split()`. For that you can follow the guidelines from <a href="https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html">sklearn train_test_split()</a>


### load_models() Method <a name = "load-models-method"></a>
- Load your models by using `load_models()` method from `ptmodels` package.

#### Arguments:
- **x_train** : provide your x_train from loaded dataset. It is required to get the `width, height and channel` of the images.
#### Example : 
```
model.load_models(x_train)
```
- This method is going to take a while for lading all the pre-trained models and their weights. You are going to see the following into your terminal.
```
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5
58889256/58889256 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/vgg19/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5
80134624/80134624 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5
94765736/94765736 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet50v2_weights_tf_dim_ordering_tf_kernels_notop.h5
94668760/94668760 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet101_weights_tf_dim_ordering_tf_kernels_notop.h5
171446536/171446536 [==============================] - 2s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet101v2_weights_tf_dim_ordering_tf_kernels_notop.h5
171317808/171317808 [==============================] - 2s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet152_weights_tf_dim_ordering_tf_kernels_notop.h5
234698864/234698864 [==============================] - 2s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet152v2_weights_tf_dim_ordering_tf_kernels_notop.h5
234545216/234545216 [==============================] - 2s 0us/step
WARNING:tensorflow:`input_shape` is undefined or non-square, or `rows` is not in [128, 160, 192, 224]. Weights for input shape (224, 224) will be loaded as the default.
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/mobilenet/mobilenet_1_0_224_tf_no_top.h5
17225924/17225924 [==============================] - 0s 0us/step
WARNING:tensorflow:`input_shape` is undefined or non-square, or `rows` is not in [96, 128, 160, 192, 224]. Weights for input shape (224, 224) will be loaded as the default.
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/mobilenet_v2/mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5
9406464/9406464 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/densenet/densenet121_weights_tf_dim_ordering_tf_kernels_notop.h5
29084464/29084464 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/densenet/densenet169_weights_tf_dim_ordering_tf_kernels_notop.h5
51877672/51877672 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/densenet/densenet201_weights_tf_dim_ordering_tf_kernels_notop.h5
74836368/74836368 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/nasnet/NASNet-mobile-no-top.h5
19993432/19993432 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/nasnet/NASNet-large-no-top.h5
343610240/343610240 [==============================] - 3s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb0_notop.h5
16705208/16705208 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb1_notop.h5
27018416/27018416 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb2_notop.h5
31790344/31790344 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb3_notop.h5
43941136/43941136 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb4_notop.h5
71686520/71686520 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb5_notop.h5
115263384/115263384 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb6_notop.h5
165234480/165234480 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/keras-applications/efficientnetb7_notop.h5
258076736/258076736 [==============================] - 2s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-b0_notop.h5
24274472/24274472 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-b1_notop.h5
28456008/28456008 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-b2_notop.h5
35839040/35839040 [==============================] - 0s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-b3_notop.h5
52606240/52606240 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-s_notop.h5
82420632/82420632 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-m_notop.h5
214201816/214201816 [==============================] - 2s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/efficientnet_v2/efficientnetv2-l_notop.h5
473176280/473176280 [==============================] - 5s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/convnext/convnext_tiny_notop.h5
111650432/111650432 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/convnext/convnext_small_notop.h5
198551472/198551472 [==============================] - 1s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/convnext/convnext_base_notop.h5
350926856/350926856 [==============================] - 3s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/convnext/convnext_large_notop.h5
785596384/785596384 [==============================] - 7s 0us/step
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/convnext/convnext_xlarge_notop.h5
 853016576/1393257616 [=================>............] - ETA: 5s
 ```
 
 
### models_name() Method <a name = "models-name-method"></a>
- `models_name()` method will let you find out the loaded models names in your class object.
- No arguments are needed for this  method. 

#### Example:
```
names = []
names = model.models_name()
print(names)
```
##### Output:
```
['VGG16', 'VGG19', 'ResNet50', 'ResNet50V2', 'ResNet101', 'ResNet101V2', 'ResNet152', 'ResNet152V2', 'MobileNet', 'MobileNetV2', 'DenseNet121', 'DenseNet169', 'EfficientNetV2B1', 'EfficientNetV2B2', 'EfficientNetV2B3', 'EfficientNetV2S', 'EfficientNetV2M', 'EfficientNetV2L', 'ConvNeXtTiny', 'ConvNeXtSmall', 'ConvNeXtBase', 'ConvNeXtLarge', 'ConvNeXtXLarge']
```
## Classification <a name = "classification"></a>
- Using `ptmodels` package you can easily train your dataset using all the pre-trained models or using any specific models. All the small tasks are done already. You just need to provide the dataset to train using this package. 
- For image classification, we are going to use two methods.
    - fit() Method
    - train_specific_model() Method
### fit() Method <a name = "fit-method"></a>
- Using this method you can very easily train your dataset using all the pre-trained models.
- That will take a lot of time.
- So our suggestion is that, use a high GPU PC or use `Google Colab` Notebook or `Kaggle` Notebook and load GPU into runtime.
#### Arguments:
- **x_train** : x_train lists the images for train datasets without labels.
- **y_train** : y_train holds the labels for train datasets.
- **x_test** : x_test has the images for test dataset without labels.
- **y_test** : y_test has the labels for the test dataset.
#### Returns:
- `pandas.dataframe` which holds the evaluation metrics of all the pre-trained models.
#### Example :
```
dataframe = model.fit(x_train, y_train, x_test, y_test)
```
- This method also saves your return dataframe into `prediction.csv` file in your disk.
![screenshot](https://raw.githubusercontent.com/rafsunsheikh/ptmodels/master/image_sources/evaluation_02.png)
##### Output:
```bash

Starting Training: VGG16
1563/1563 [==============================] - 24s 10ms/step - loss: 0.2274 - accuracy: 0.5063
1563/1563 [==============================] - 11s 7ms/step
313/313 [==============================] - 2s 7ms/step
appended successfully

Starting Training: VGG19
1563/1563 [==============================] - 19s 11ms/step - loss: 0.2313 - accuracy: 0.4969
1563/1563 [==============================] - 14s 9ms/step
313/313 [==============================] - 3s 9ms/step
appended successfully

Starting Training: ResNet50
1563/1563 [==============================] - 27s 14ms/step - loss: 0.2331 - accuracy: 0.4970
1563/1563 [==============================] - 18s 10ms/step
313/313 [==============================] - 4s 12ms/step
appended successfully

Starting Training: ResNet50V2
1563/1563 [==============================] - 26s 14ms/step - loss: 0.2843 - accuracy: 0.3291
1563/1563 [==============================] - 17s 10ms/step
313/313 [==============================] - 3s 10ms/step
appended successfully

Starting Training: ResNet101
1563/1563 [==============================] - 43s 23ms/step - loss: 0.2363 - accuracy: 0.4896
1563/1563 [==============================] - 31s 18ms/step
313/313 [==============================] - 6s 20ms/step
appended successfully

Starting Training: ResNet101V2
1563/1563 [==============================] - 43s 22ms/step - loss: 0.2923 - accuracy: 0.3033
1563/1563 [==============================] - 30s 18ms/step
313/313 [==============================] - 6s 19ms/step
appended successfully

Starting Training: ResNet152
1563/1563 [==============================] - 61s 32ms/step - loss: 0.2327 - accuracy: 0.5006
1563/1563 [==============================] - 44s 26ms/step
313/313 [==============================] - 9s 28ms/step
appended successfully

Starting Training: ResNet152V2
1563/1563 [==============================] - 62s 33ms/step - loss: 0.2959 - accuracy: 0.3003
1563/1563 [==============================] - 44s 26ms/step
313/313 [==============================] - 9s 27ms/step
appended successfully

Starting Training: MobileNet
1563/1563 [==============================] - 14s 8ms/step - loss: 0.3206 - accuracy: 0.1784
1563/1563 [==============================] - 8s 5ms/step
313/313 [==============================] - 2s 5ms/step
appended successfully

Starting Training: MobileNetV2
1563/1563 [==============================] - 20s 11ms/step - loss: 0.3165 - accuracy: 0.1961
1563/1563 [==============================] - 13s 8ms/step
313/313 [==============================] - 2s 7ms/step
appended successfully

Starting Training: DenseNet121
1563/1563 [==============================] - 42s 21ms/step - loss: 0.2424 - accuracy: 0.4628
1563/1563 [==============================] - 30s 18ms/step
313/313 [==============================] - 6s 19ms/step
appended successfully

Starting Training: DenseNet169
1563/1563 [==============================] - 55s 28ms/step - loss: 0.2432 - accuracy: 0.4567
1563/1563 [==============================] - 41s 24ms/step
313/313 [==============================] - 7s 23ms/step
appended successfully

Starting Training: EfficientNetV2B1
1563/1563 [==============================] - 33s 14ms/step - loss: 0.2233 - accuracy: 0.5198
1563/1563 [==============================] - 28s 17ms/step
313/313 [==============================] - 5s 15ms/step
appended successfully

Starting Training: EfficientNetV2B2
1563/1563 [==============================] - 35s 15ms/step - loss: 0.2279 - accuracy: 0.5117
1563/1563 [==============================] - 29s 17ms/step
313/313 [==============================] - 5s 16ms/step
appended successfully

Starting Training: EfficientNetV2B3
1563/1563 [==============================] - 39s 17ms/step - loss: 0.2584 - accuracy: 0.4208
1563/1563 [==============================] - 34s 20ms/step
313/313 [==============================] - 6s 19ms/step
appended successfully

Starting Training: EfficientNetV2S
1563/1563 [==============================] - 47s 20ms/step - loss: 0.2455 - accuracy: 0.4598
1563/1563 [==============================] - 43s 25ms/step
313/313 [==============================] - 7s 24ms/step
appended successfully

Starting Training: EfficientNetV2M
1563/1563 [==============================] - 66s 28ms/step - loss: 0.3221 - accuracy: 0.2315
1563/1563 [==============================] - 60s 35ms/step
313/313 [==============================] - 11s 35ms/step
appended successfully

Starting Training: EfficientNetV2L
1563/1563 [==============================] - 95s 40ms/step - loss: 0.2644 - accuracy: 0.4007
1563/1563 [==============================] - 83s 48ms/step
313/313 [==============================] - 15s 48ms/step
appended successfully

Starting Training: ConvNeXtTiny
1563/1563 [==============================] - 60s 30ms/step - loss: 0.1644 - accuracy: 0.6741
1563/1563 [==============================] - 45s 27ms/step
313/313 [==============================] - 9s 27ms/step
appended successfully

Starting Training: ConvNeXtSmall
1563/1563 [==============================] - 103s 53ms/step - loss: 0.1573 - accuracy: 0.6885
1563/1563 [==============================] - 83s 49ms/step
313/313 [==============================] - 16s 50ms/step
appended successfully

Starting Training: ConvNeXtBase
1563/1563 [==============================] - 105s 54ms/step - loss: 0.1435 - accuracy: 0.7221
1563/1563 [==============================] - 83s 50ms/step
313/313 [==============================] - 15s 48ms/step
appended successfully

Starting Training: ConvNeXtLarge
1563/1563 [==============================] - 117s 62ms/step - loss: 0.1237 - accuracy: 0.7662
1563/1563 [==============================] - 91s 55ms/step
313/313 [==============================] - 18s 58ms/step
appended successfully

Starting Training: ConvNeXtXLarge
1563/1563 [==============================] - 129s 69ms/step - loss: 0.1178 - accuracy: 0.7845
1563/1563 [==============================] - 104s 63ms/step
313/313 [==============================] - 20s 64ms/step
appended successfully

              Models Accuracy train Precision train Recall train  \
0              VGG16          0.621           0.621        0.621   
1              VGG19          0.602           0.602        0.602   
2           ResNet50          0.622           0.622        0.622   
3         ResNet50V2          0.412           0.412        0.412   
4          ResNet101          0.614           0.614        0.614   
5        ResNet101V2          0.386           0.386        0.386   
6          ResNet152          0.622           0.622        0.622   
7        ResNet152V2          0.379           0.379        0.379   
8          MobileNet          0.205           0.205        0.205   
9        MobileNetV2          0.234           0.234        0.234   
10       DenseNet121          0.578           0.578        0.578   
11       DenseNet169          0.557           0.557        0.557   
12  EfficientNetV2B1          0.652           0.652        0.652   
13  EfficientNetV2B2          0.641           0.641        0.641   
14  EfficientNetV2B3          0.593           0.593        0.593   
15   EfficientNetV2S          0.610           0.610        0.610   
16   EfficientNetV2M          0.384           0.384        0.384   
17   EfficientNetV2L          0.561           0.561        0.561   
18      ConvNeXtTiny          0.776           0.776        0.776   
19     ConvNeXtSmall          0.786           0.786        0.786   
20      ConvNeXtBase          0.815           0.815        0.815   
21     ConvNeXtLarge          0.855           0.855        0.855   
22    ConvNeXtXLarge          0.863           0.863        0.863   

   f1_score train Accuracy test Precision test Recall test f1_score test  
0           0.621         0.595          0.595       0.595         0.595  
1           0.602         0.585          0.585       0.585         0.585  
2           0.622         0.594          0.594       0.594         0.594  
3           0.412         0.397          0.397       0.397         0.397  
4           0.614         0.578          0.578       0.578         0.578  
5           0.386         0.382          0.382       0.382         0.382  
6           0.622         0.590          0.590       0.590         0.590  
7           0.379         0.367          0.367       0.367         0.367  
8           0.205         0.201          0.201       0.201         0.201  
9           0.234         0.230          0.230       0.230         0.230  
10          0.578         0.553          0.553       0.553         0.553  
11          0.557         0.539          0.539       0.539         0.539  
12          0.652         0.631          0.631       0.631         0.631  
13          0.641         0.630          0.630       0.630         0.630  
14          0.593         0.583          0.583       0.583         0.583  
15          0.610         0.601          0.601       0.601         0.601  
16          0.384         0.381          0.381       0.381         0.381  
17          0.561         0.547          0.547       0.547         0.547  
18          0.776         0.740          0.740       0.740         0.740  
19          0.786         0.759          0.759       0.759         0.759  
20          0.815         0.785          0.785       0.785         0.785  
21          0.855         0.829          0.829       0.829         0.829  
22          0.863         0.831          0.831       0.831         0.831  
```
### train_specific_model() Method <a name = "train-specific-model-method"></a>
- You can train your dataset on a specific model using this method. 
- You just have to specify the `model_name`.
- The method will return the evaluation metrics of the trained model.

#### Arguments:
- **x_train** : x_train lists the images for train datasets without labels.
- **y_train** : y_train holds the labels for train datasets.
- **x_test** : x_test has the images for test dataset without labels.
- **y_test** : y_test has the labels for the test dataset.
-  model_name
- **num_classes** : Takes the number of classes for classification. Default value is set to **2**.
- **batch_size** : Trains the image dataset into batches. Defaults Batch size value is **32**.
- **epochs** : Takes the number of number of epochs for the training. Default value set to **1**.
- **learning_rate** : Sets the learning rate for training the model. Default value set to **1e-4**. 
- **momentum** : Sets the value of momentum for training the model. Default value set to **0.9**.
-  **SAVE_MODEL** : This is a `boolean` argument which tells the method to save the `model` and `model weight` to file or not. The default value is set to **False**.

#### Return:
- `pandas.dataframe` that holds the evaluation metrics of the specific model on the image dataset.
#### Example: 
```
df_VGG16 = model.train_specific_model( x_train, y_train, x_test, y_test, model_name, num_classes=10, batch_size=32, epochs=20, learning_rate=1e-4, momentum=0.9, SAVE_MODEL = True)
```
##### Output:
```
1563/1563 [==============================] - 37s 17ms/step - loss: 0.3047 - accuracy: 0.3329
Saved model to disk
1563/1563 [==============================] - 12s 7ms/step
313/313 [==============================] - 2s 7ms/step
```

## Evaluation <a name = "evaluation"></a>
- You can easily load the specific model and the weights from the disk and evaluate using test dataset.
- You can evaluate the model using two simple methods as:
    - evaluate_saved_model() Method
    - predict_image_saved_model() Method.

### evaluate_saved_model() Method <a name = "evaluate-saved-model-method"></a>
- This method simple tells you the accuracy of the saved model.
#### Arguments:
- **x_test** : x_test has the images for test dataset without labels.
- **y_test** : y_test has the labels for the test dataset.
#### Example:
```
model.evaluate_saved_model(x_test, y_test)
```
##### Output:
```
Loaded model from disk
accuracy: 53.04%
```

### predict_image_saved_model() Method <a name = "predict-image-saved-model-method"></a>

#### Arguments
- **image_path** : You have to provide the image path of your single image that you want to evaluate.
- **image_width** : You have to provide the image width on which your specific model is trained on.
- **image_height** : You have to provide the image height on which your specific model is trained on. 
#### Example:
```
image_path  = '/content/maple.jpg'
image_width = 32
image_height = 32
prediction = model.predict_image_saved_model(image_path, image_width, image_height)
```
- In this example we are providing the `image_width` and `image_height` as both `32`, as our model is trained on `32x32` images.
##### Output:
```
Loaded model from disk

1/1 [==============================] - 0s 334ms/step
[[0.09631938 0.08813578 0.02288193 0.03976142 0.07516313 0.1624043
  0.04893952 0.16084285 0.04286739 0.26268432]]
```
- You can use this prediction for further evaluation like you can use `argmax()` method to get the highest value and also you can map the value with label names.

## Credits <a name = "credits"></a>

This software uses the following open source packages:

- [Tensorflow](https://tensorflow.org/)
- [Keras](https://keras.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)
- [highlight.js](https://highlightjs.org/)

## Related <a name = "related"></a>

[LazyPredict](https://github.com/shankarpandala/lazypredict) - Classification using basic models

## Support <a name = "support"></a>

<a href="https://www.buymeacoffee.com/rafsunSheikh" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/LevDropStudio">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like... <a name = "you-may-also-like"></a>

- [Signature Fraud Detection](https://github.com/rafsunsheikh/signatureFraud) - A Django app to detect signature fraud from Bank checks.
- [AIST](https://github.com/rafsunsheikh/IDP_AIST) - Artificial Intelligence Surveillance Tower
- [Parliament Bhaban](https://github.com/rafsunsheikh/openGL_project) - A fun OpenGL project for 2D animation.
- [Mancala](https://github.com/rafsunsheikh/mancala_repo) - A simple AI Mancala game built in Python

## License <a name = "license"></a>

MIT

---

> [rafsunsheikh.github.io/Web](https://rafsunsheikh.github.io/Web) &nbsp;&middot;&nbsp;
> GitHub [@rafsunsheikh](https://github.com/rafsunsheikh) &nbsp;&middot;&nbsp;
> Twitter [@RafsunSheikh](https://twitter.com/RafsunSheikh) &nbsp;&middot;&nbsp;
> LinkedIn [@md-rafsun-sheikh](https://www.linkedin.com/in/md-rafsun-sheikh-b3898882/)

