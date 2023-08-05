import setuptools
from DePTH import __version__

with open("DESCRIPTION", "r", encoding = "utf-8") as fh:
    long_description = fh.read()



seeds_list = [['5779', '7821', '6367'],
             ['4230', '6476', '5126'],
             ['1383', '4065', '6352'],
             ['1729', '4240', '6624'],
             ['6032', '2168', '8056'],
             ['1608', '8784', '6229'],
             ['3418', '1359', '9143'],
             ['4920', '7053', '8233'],
             ['2685', '7038', '9634'],
             ['5745', '1179', '2345'],
             ['4469', '6840', '2514'],
             ['483', '5009', '1203'],
             ['2569', '2343', '341'],
             ['7413', '4849', '3117'],
             ['3508', '5011', '7339'],
             ['9193', '7966', '7633'],
             ['9416', '7885', '479'],
             ['601', '2186', '4976'],
             ['2249', '2812', '8150'],
             ['5446', '2204', '6820']]


data_file_list = ['data/for_encoders/*.csv', \
                  'data/for_encoders/*.tsv']

for cur_seeds in seeds_list:
    for core_name in ["HLA_I_all_match", "HLA_II_all_match"]:
        full_name = core_name+"_model_"+"_".join(cur_seeds)
        data_file_list += \
             ['data/trained_models/'+core_name+'/'+full_name+'/assets/*', \
              'data/trained_models/'+core_name+'/'+full_name+'/fingerprint.pb', \
              'data/trained_models/'+core_name+'/'+full_name+'/keras_metadata.pb', \
              'data/trained_models/'+core_name+'/'+full_name+'/saved_model.pb', \
              'data/trained_models/'+core_name+'/'+full_name+'/variables/*']

setuptools.setup(
    name = "DePTH",
    version = __version__,
    author="Si Liu",
    author_email="liusi2019@gmail.com",
    description = "DePTH provides neural network models for sequence-based TCR and HLA association prediction",
    long_description = long_description,
    long_description_content_type = "text/plain",
    url = "https://github.com/Sun-lab/DePTH",
    project_urls = {
        "Documentation": "https://github.com/Sun-lab/DePTH",
        "Bug Tracker": "https://github.com/Sun-lab/DePTH/issues",
    },
    license='MIT',
    entry_points={
        "console_scripts": ["DePTH=DePTH.main:main"]
        },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    #packages = setuptools.find_packages(where="DePTH"),
    #packages = ["DePTH"],
    packages = setuptools.find_packages(),
    include_package_data=True,
    package_data={'DePTH': data_file_list},
    python_requires = ">=3.9",
    install_requires=[
        'scikit-learn >= 1.0.2',
        'tensorflow >= 2.4.1',
        'pandas >= 1.4.2',
        'numpy >= 1.21.5',
        ]
)
