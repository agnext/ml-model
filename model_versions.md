## Classification -- Famoso  [Non-pareil]

- model_410<stale> -1 (checksum - 
2819381443 287377826 almonds_defect_classification_graph/1/saved_model.pb)

-  model_185<BROKEN> - 2 (checksum - 
936041026 287377826 almonds_defect_classification_graph/2/saved_model.pb)

- model_185(inception) - 3 (checksum - 
2819381443 287377826 almonds_defect_classification_graph/3/saved_model.pb)

- model_214(inception blue diamond demo) - 4 (checksum - 
3360217221 287377826 almonds_defect_classification_graph/4/saved_model.pb)

- model_245(inception famoso demo feb17) - 5 (checksum - 
1589621032 287377826 almonds_defect_classification_graph/5/saved_model.pb)

- model_717(inception famoso demo march 4) - 6 (checksum - 
3198672060 287377826 almonds_defect_classification_graph/6/saved_model.pb)

- model_712(inception 18 class individual defects) - 7 (checksum - 
223767645 287439326 almonds_defect_classification_graph/7/saved_model.pb)

- model_910(inception 19 class individual defects) -8 (checksum - 
2784077183 287451626 almonds_defect_classification_graph/8/saved_model.pb)
<br>

- model_932(trained with unit 15 data) - 9 (checksum - 
1915877582 287453452 almonds_defect_classification_graph/9/saved_model.pb)


#### Famoso Ensemble v1 - May 08
Rotation factor: 4
- almonds_defect_classification_graph [8] -- inception [Internal ver 910]
- almonds_defect_classification_res [1] -- resnet [Internal ver 251]
- almonds_defect_classification_vgg [1] -- vgg [Internal ver 297]


#### Famoso Ensemble v2 - May 09
Rotation factor: 4
- almonds_defect_classification_graph [10] -- inception [Internal ver 1090]
- almonds_defect_classification_res [2] -- resnet [Internal ver 377]
- almonds_defect_classification_vgg [2] -- vgg [Internal ver 352]


#### Famoso Ensemble v4 - Jun 18
Rotation factor: 1
- almond_classification_model_ensemble [4] -- 
Combination of inception, resnet, vgg with 4 rotations in single pass

Rotation factor: 4
- almonds_defect_classification_graph [11] -- inception [Internal ver 1962]
- almonds_defect_classification_res [4] -- resnet [Internal ver 868]
- almonds_defect_classification_vgg [4] -- vgg [Internal ver 823]

#### Famoso Ensemble v5 - July 7, 2020
Rotation factor: 4
- 12 models - 4 versions of inception, resnet and vgg each.
- Internal model numbers:
  - inception_v3 [1962, 2234_1, 2418_1, 2541_0]
  - resnet50 [969_1, 1016_1, 1068_1, 1107_1]
  - vgg16 [823_0, 824_1, 1079_0, 1285_0]
- cksum almonds_defect_classification_ensemble/5/saved_model.pb<br>
2352443236 1041976768 almonds_defect_classification_ensemble/5/saved_model.pb

#### Famoso Ensemble v6 - Aug 4, 2020
Rotation factor: 4
- 12 models - 4 versions of inception, resnet and vgg each.
- Models trained from scratch. Internal model numbers:
  - inception_v3 [20200731_1_a_1/223_0, 20200731_1_a_1_y/237_0, 20200731_1_a_1_y/253_0, 20200731_1_a_1_y/266_0]
  - resnet50 [20200731_1_a_1/325_0, 20200731_1_a_1/366_0, 20200731_1_a_1/394_0, 20200731_1_a_2/438_0]
  - vgg16 [20200731_1_a_1/281_0, 20200731_1_a_1/310_0, 20200731_1_b_1/324_0, 20200731_3_a/241_0]
- Add uniformity to defect list. Total defect count for famoso increases to 20
- cksum almonds_defect_classification_ensemble/6/saved_model.pb<br>
1535480116 1042025968 almonds_defect_classification_ensemble_famoso/6/saved_model.pb


## Classification -- Famoso  [Independence]
#### Ensemble v1 - Nov 16, 2020
Rotation factor: 4
- 12 models - 4 versions of inception, resnet and vgg each.
- Internal Experiment Version: 11014 [ensv1 - trial4 (v1_ind_t4)]
  Internal model numbers:
  - inception_v3 [20201112_1_a_1/111_0, 20201112_1_a/91_0, 20201112_1_a/179_0, 20201112_1_a/187_0]
  - resnet50 [20201112_1_a_1/325_0, 20201112_1_a/133_0, 20201112_1_b_1/238_0, 20201112_1_b_2/355_0]
  - vgg16 [20201112_1_b_1/186_0, 20201112_1_b_1/206_0, 20201112_1_b_3/367_0, 20201112_2_b_1/533_0]
- First independence model in production
- cksum almonds_defect_classification_ensemble_famoso_ind/1/saved_model.pb<br>
664677894 1042025968 almonds_defect_classification_ensemble_famoso_ind/1/saved_model.pb


## Classification -- Famoso  [Monterey]
#### Ensemble v1 - Mar 03, 2021
Rotation factor: 4
- 12 models - 4 versions of inception, resnet and vgg each.
- Internal Experiment Version: 11015 [ensv1 - trial5 (v1_mnt_t5)]
  Internal model numbers:
  - inception_v3 [20210225_1_b_1/189_0, 20210225_1_b_1/261_0, 20210225_1_a_1/265_0, 20210225_1_b/303_0]
  - resnet50 [20210225_1_b/254_0, 20210225_1_a_1/455_0, 20210225_1_b_1/398_0, 20210225_1_a/301_0]
  - vgg16 [20210225_1_a/229_0, 20210225_1_c/382_0, 20210225_1_b/268_0, 20210225_2/496_0]
- First monterey model in production
- cksum almonds_defect_classification_ensemble_famoso_mnt/1/saved_model.pb<br>
2376383734 1042025965 almonds_defect_classification_ensemble_famoso_mnt/1/saved_model.pb


## Classification -- Harriswoolf

#### Harriswoolf Ensemble v1 - Aug 21, 2020
Rotation factor: 4
- Internal version - v1_trial1 (11010)
- 12 models - 2 versions of inception, resnet and vgg each, 2 rotation for each
- Models trained from scratch. Internal model numbers:
  - inception_v3 [20200806_1_a_1/174_0, 20200806_1_a_2/400_0, 20200806_1_a/155_0, 20200806_1_a/157_0]
  - resnet50 [20200806_1_a_1/362_0, 20200806_1_a_2/465_0, 20200806_1_a/304_0, 20200806_1_a/327_0]
  - vgg16 [20200806_1_a/181_0, 20200806_1_a/238_0, 20200806_2_a_1/206_0, 20200806_2_a/224_0]

- cksum almonds_defect_classification_ensemble_harris/1/saved_model.pb<br>
2182502271 1042025968 almonds_defect_classification_ensemble_harris/1/saved_model.pb

#### Harriswoolf Ensemble v2 - Aug 21, 2020
Rotation factor: 4
- Internal version - v2_trial2 (11022)
- 12 models - 4 versions of inception, resnet and vgg each (each with different rotation)
- Models trained  in continuation of Ensemble v1
  - inception_v3 [20200818_1_a_1/653_0, 20200818_1_a_1/716_0, 20200818_1_a_2/565_0, 20200818_1_a/519_0]
  - resnet50 [20200818_1_a_2/850_0, 20200818_1_a_2/974_0, 20200818_1_a/670_0, 20200818_1/436_0]
  - vgg16 [20200818_1_a_1/338_0, 20200818_1_a_2/324_0, 20200818_1_a_2/340_0, 20200818_2_a/339_0]
- Train model with mix of harriswoolf and partly famoso data for certain defects
```
        total   harriswoolf famoso
frass	6000	3000		3000
insect	6000	3000		3000
chip	6000	3000		3000
good	29000	25000		10000
```
- cksum almonds_defect_classification_ensemble_harris/2/saved_model.pb<br>
1843271763 1042025968 almonds_defect_classification_ensemble_harris/2/saved_model.pb


## Segmentation

 - model_52(Multipass-Resnet101) - 1 (checksum - 
 2613252321 255409205 almond_segmentation_mrcnn_model/1/saved_model.pb)
            
  - model_54(SinglePass-Resnet50) - 2 (checksum - 
  3871294580 178996330 almond_segmentation_mrcnn_model/2/saved_model.pb)
  
 - model (SinglePass-Resnet50) - 3 [Internal ver: 20200726/50] (checksum - 
 2696003270 178996330 almond_segmentation_mrcnn_model/3/saved_model.pb
   - Improved detection for foreign materials, uniformity & densely packed almonds.


