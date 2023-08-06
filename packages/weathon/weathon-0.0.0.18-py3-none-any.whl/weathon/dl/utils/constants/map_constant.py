from weathon.dl.utils.constants.constants import Metrics, Preprocessors, TaskModels, Tasks, Models, Pipelines

task_default_metrics = {
    Tasks.image_segmentation: [Metrics.image_ins_seg_coco_metric],
    Tasks.sentence_similarity: [Metrics.seq_cls_metric],
    Tasks.nli: [Metrics.seq_cls_metric],
    Tasks.sentiment_classification: [Metrics.seq_cls_metric],
    Tasks.token_classification: [Metrics.token_cls_metric],
    Tasks.text_generation: [Metrics.text_gen_metric],
    Tasks.chat: [Metrics.text_gen_metric],
    Tasks.text_classification: [Metrics.seq_cls_metric],
    Tasks.image_denoising: [Metrics.image_denoise_metric],
    Tasks.image_deblurring: [Metrics.image_denoise_metric],
    Tasks.video_super_resolution: [Metrics.video_super_resolution_metric],
    Tasks.image_color_enhancement: [Metrics.image_color_enhance_metric],
    Tasks.image_portrait_enhancement:
    [Metrics.image_portrait_enhancement_metric],
    Tasks.video_summarization: [Metrics.video_summarization_metric],
    Tasks.image_captioning: [Metrics.accuracy],
    Tasks.visual_question_answering: [Metrics.accuracy],
    Tasks.movie_scene_segmentation: [Metrics.movie_scene_segmentation_metric],
    Tasks.image_inpainting: [Metrics.image_inpainting_metric],
    Tasks.referring_video_object_segmentation:
    [Metrics.referring_video_object_segmentation_metric],
    Tasks.video_frame_interpolation:
    [Metrics.video_frame_interpolation_metric],
    Tasks.video_stabilization: [Metrics.video_stabilization_metric],
    Tasks.image_quality_assessment_degradation:
    [Metrics.image_quality_assessment_degradation_metric],
    Tasks.image_quality_assessment_mos:
    [Metrics.image_quality_assessment_mos_metric],
    Tasks.bad_image_detecting: [Metrics.accuracy],
    Tasks.ocr_recognition: [Metrics.ocr_recognition_metric],
    Tasks.efficient_diffusion_tuning: [Metrics.loss_metric],
    Tasks.translation_evaluation: [Metrics.translation_evaluation_metric]
}




PREPROCESSOR_MAP = {
    # nlp
    (Models.canmt, Tasks.competency_aware_translation): Preprocessors.canmt_translation,
    # bart
    (Models.bart, Tasks.text_error_correction):Preprocessors.text_error_correction,

    # bert
    (Models.bert, Tasks.backbone): Preprocessors.sen_cls_tokenizer,
    (Models.bert, Tasks.document_segmentation): Preprocessors.document_segmentation,
    (Models.bert, Tasks.fill_mask): Preprocessors.fill_mask,
    (Models.bert, Tasks.sentence_embedding): Preprocessors.sentence_embedding,
    (Models.bert, Tasks.text_classification): Preprocessors.sen_cls_tokenizer,
    (Models.bert, Tasks.nli): Preprocessors.sen_cls_tokenizer,
    (Models.bert, Tasks.sentiment_classification): Preprocessors.sen_cls_tokenizer,
    (Models.bert, Tasks.sentence_similarity): Preprocessors.sen_cls_tokenizer,
    (Models.bert, Tasks.zero_shot_classification): Preprocessors.sen_cls_tokenizer,
    (Models.bert, Tasks.text_ranking): Preprocessors.text_ranking,
    (Models.bert, Tasks.part_of_speech): Preprocessors.token_cls_tokenizer,
    (Models.bert, Tasks.token_classification): Preprocessors.token_cls_tokenizer,
    (Models.bert, Tasks.word_segmentation): Preprocessors.token_cls_tokenizer,

    # bloom
    (Models.bloom, Tasks.backbone): Preprocessors.text_gen_tokenizer,

    # gpt_neo
    # gpt_neo may have different preprocessors, but now only one
    (Models.gpt_neo, Tasks.backbone): Preprocessors.sentence_piece,

    # gpt3 has different preprocessors by different sizes of models, so they are not listed here.

    # palm_v2
    (Models.palm, Tasks.backbone): Preprocessors.text_gen_tokenizer,

    # T5
    (Models.T5, Tasks.backbone): Preprocessors.text2text_gen_preprocessor,
    (Models.T5, Tasks.text2text_generation): Preprocessors.text2text_gen_preprocessor,

    # deberta_v2
    (Models.deberta_v2, Tasks.backbone): Preprocessors.sen_cls_tokenizer,
    (Models.deberta_v2, Tasks.fill_mask): Preprocessors.fill_mask,

    # ponet
    (Models.ponet, Tasks.fill_mask): Preprocessors.fill_mask_ponet,

    # structbert
    (Models.structbert, Tasks.backbone): Preprocessors.sen_cls_tokenizer,
    (Models.structbert, Tasks.fill_mask): Preprocessors.fill_mask,
    (Models.structbert, Tasks.faq_question_answering): Preprocessors.faq_question_answering_preprocessor,
    (Models.structbert, Tasks.text_classification): Preprocessors.sen_cls_tokenizer,
    (Models.structbert, Tasks.nli): Preprocessors.sen_cls_tokenizer,
    (Models.structbert, Tasks.sentiment_classification):  Preprocessors.sen_cls_tokenizer,
    (Models.structbert, Tasks.sentence_similarity): Preprocessors.sen_cls_tokenizer,
    (Models.structbert, Tasks.zero_shot_classification): Preprocessors.sen_cls_tokenizer,
    (Models.structbert, Tasks.part_of_speech): Preprocessors.token_cls_tokenizer,
    (Models.token_classification_for_ner, Tasks.named_entity_recognition):  Preprocessors.token_cls_tokenizer,
    (Models.structbert, Tasks.token_classification): Preprocessors.token_cls_tokenizer,
    (Models.structbert, Tasks.word_segmentation): Preprocessors.token_cls_tokenizer,

    # doc2bot
    (Models.doc2bot, Tasks.document_grounded_dialog_generate): Preprocessors.document_grounded_dialog_generate,
    (Models.doc2bot, Tasks.document_grounded_dialog_rerank):  Preprocessors.document_grounded_dialog_rerank,
    (Models.doc2bot, Tasks.document_grounded_dialog_retrieval): Preprocessors.document_grounded_dialog_retrieval,

    # veco
    (Models.veco, Tasks.backbone): Preprocessors.sen_cls_tokenizer,
    (Models.veco, Tasks.fill_mask): Preprocessors.fill_mask,
    (Models.veco, Tasks.text_classification): Preprocessors.sen_cls_tokenizer,
    (Models.veco, Tasks.nli): Preprocessors.sen_cls_tokenizer,
    (Models.veco, Tasks.sentiment_classification):  Preprocessors.sen_cls_tokenizer,
    (Models.veco, Tasks.sentence_similarity): Preprocessors.sen_cls_tokenizer,

    # ner models
    (Models.lcrf, Tasks.named_entity_recognition): Preprocessors.sequence_labeling_tokenizer,
    (Models.lcrf, Tasks.word_segmentation): Preprocessors.sequence_labeling_tokenizer,
    (Models.lcrf, Tasks.part_of_speech): Preprocessors.sequence_labeling_tokenizer,
    (Models.lcrf_wseg, Tasks.word_segmentation): Preprocessors.sequence_labeling_tokenizer,
    (Models.tcrf_wseg, Tasks.word_segmentation): Preprocessors.sequence_labeling_tokenizer,
    (Models.tcrf, Tasks.named_entity_recognition): Preprocessors.sequence_labeling_tokenizer,

    # task models
    (TaskModels.token_classification, Tasks.token_classification): Preprocessors.sequence_labeling_tokenizer,
    (TaskModels.token_classification, Tasks.part_of_speech): Preprocessors.sequence_labeling_tokenizer,
    (TaskModels.token_classification, Tasks.named_entity_recognition): Preprocessors.sequence_labeling_tokenizer,
    (TaskModels.text_classification, Tasks.text_classification): Preprocessors.sen_cls_tokenizer,
    (TaskModels.fill_mask, Tasks.fill_mask): Preprocessors.fill_mask,
    (TaskModels.feature_extraction, Tasks.feature_extraction): Preprocessors.feature_extraction,
    (TaskModels.information_extraction, Tasks.information_extraction): Preprocessors.re_tokenizer,
    (TaskModels.text_ranking, Tasks.text_ranking): Preprocessors.text_ranking,
    (TaskModels.text_generation, Tasks.text_generation): Preprocessors.text_gen_tokenizer,

    # cv
    (Models.tinynas_detection, Tasks.image_object_detection): Preprocessors.object_detection_tinynas_preprocessor,
    (Models.tinynas_damoyolo, Tasks.image_object_detection): Preprocessors.object_detection_tinynas_preprocessor,
    (Models.tinynas_damoyolo, Tasks.domain_specific_object_detection): Preprocessors.object_detection_tinynas_preprocessor,
    (Models.controllable_image_generation, Tasks.controllable_image_generation):  Preprocessors.controllable_image_generation_preprocessor,
}



DEFAULT_MODEL_FOR_PIPELINE = {
    # TaskName: (pipeline_module_name, model_repo)
    Tasks.sentence_embedding:
    (Pipelines.sentence_embedding,
     'damo/nlp_corom_sentence-embedding_english-base'),
    Tasks.text_ranking: (Pipelines.mgeo_ranking,
                         'damo/mgeo_address_ranking_chinese_base'),
    Tasks.text_ranking: (Pipelines.text_ranking,
                         'damo/nlp_corom_passage-ranking_english-base'),
    Tasks.word_segmentation:
    (Pipelines.word_segmentation,
     'damo/nlp_structbert_word-segmentation_chinese-base'),
    Tasks.part_of_speech: (Pipelines.part_of_speech,
                           'damo/nlp_structbert_part-of-speech_chinese-base'),
    Tasks.token_classification:
    (Pipelines.part_of_speech,
     'damo/nlp_structbert_part-of-speech_chinese-base'),
    Tasks.named_entity_recognition:
    (Pipelines.named_entity_recognition,
     'damo/nlp_raner_named-entity-recognition_chinese-base-news'),
    Tasks.relation_extraction:
    (Pipelines.relation_extraction,
     'damo/nlp_bert_relation-extraction_chinese-base'),
    Tasks.information_extraction:
    (Pipelines.relation_extraction,
     'damo/nlp_bert_relation-extraction_chinese-base'),
    Tasks.sentence_similarity:
    (Pipelines.sentence_similarity,
     'damo/nlp_structbert_sentence-similarity_chinese-base'),
    Tasks.competency_aware_translation:
    (Pipelines.canmt_translation, 'damo/nlp_canmt_translation_zh2en_large'),
    Tasks.translation: (Pipelines.csanmt_translation,
                        'damo/nlp_csanmt_translation_zh2en'),
    Tasks.nli: (Pipelines.nli, 'damo/nlp_structbert_nli_chinese-base'),
    Tasks.sentiment_classification:
    (Pipelines.sentiment_classification,
     'damo/nlp_structbert_sentiment-classification_chinese-base'
     ),  # TODO: revise back after passing the pr
    Tasks.portrait_matting: (Pipelines.portrait_matting,
                             'damo/cv_unet_image-matting'),
    Tasks.universal_matting: (Pipelines.universal_matting,
                              'damo/cv_unet_universal-matting'),
    Tasks.human_detection: (Pipelines.human_detection,
                            'damo/cv_resnet18_human-detection'),
    Tasks.image_object_detection: (Pipelines.object_detection,
                                   'damo/cv_vit_object-detection_coco'),
    Tasks.image_denoising: (Pipelines.image_denoise,
                            'damo/cv_nafnet_image-denoise_sidd'),
    Tasks.image_deblurring: (Pipelines.image_deblur,
                             'damo/cv_nafnet_image-deblur_gopro'),
    Tasks.video_stabilization: (Pipelines.video_stabilization,
                                'damo/cv_dut-raft_video-stabilization_base'),
    Tasks.video_super_resolution:
    (Pipelines.video_super_resolution,
     'damo/cv_realbasicvsr_video-super-resolution_videolq'),
    Tasks.text_classification:
    (Pipelines.sentiment_classification,
     'damo/nlp_structbert_sentiment-classification_chinese-base'),
    Tasks.text_generation: (Pipelines.text_generation,
                            'damo/nlp_palm2.0_text-generation_chinese-base'),
    Tasks.zero_shot_classification:
    (Pipelines.zero_shot_classification,
     'damo/nlp_structbert_zero-shot-classification_chinese-base'),
    Tasks.task_oriented_conversation: (Pipelines.dialog_modeling,
                                       'damo/nlp_space_dialog-modeling'),
    Tasks.dialog_state_tracking: (Pipelines.dialog_state_tracking,
                                  'damo/nlp_space_dialog-state-tracking'),
    Tasks.table_question_answering:
    (Pipelines.table_question_answering_pipeline,
     'damo/nlp-convai-text2sql-pretrain-cn'),
    Tasks.document_grounded_dialog_generate:
    (Pipelines.document_grounded_dialog_generate,
     'DAMO_ConvAI/nlp_convai_generation_pretrain'),
    Tasks.document_grounded_dialog_rerank:
    (Pipelines.document_grounded_dialog_rerank,
     'damo/nlp_convai_rerank_pretrain'),
    Tasks.document_grounded_dialog_retrieval:
    (Pipelines.document_grounded_dialog_retrieval,
     'DAMO_ConvAI/nlp_convai_retrieval_pretrain'),
    Tasks.text_error_correction:
    (Pipelines.text_error_correction,
     'damo/nlp_bart_text-error-correction_chinese'),
    Tasks.image_captioning: (Pipelines.image_captioning,
                             'damo/ofa_image-caption_coco_large_en'),
    Tasks.video_captioning:
    (Pipelines.video_captioning,
     'damo/multi-modal_hitea_video-captioning_base_en'),
    Tasks.image_portrait_stylization:
    (Pipelines.person_image_cartoon,
     'damo/cv_unet_person-image-cartoon_compound-models'),
    Tasks.ocr_detection: (Pipelines.ocr_detection,
                          'damo/cv_resnet18_ocr-detection-line-level_damo'),
    Tasks.table_recognition:
    (Pipelines.table_recognition,
     'damo/cv_dla34_table-structure-recognition_cycle-centernet'),
    Tasks.lineless_table_recognition:
    (Pipelines.lineless_table_recognition,
     'damo/cv_resnet-transformer_table-structure-recognition_lore'),
    Tasks.document_vl_embedding:
    (Pipelines.document_vl_embedding,
     'damo/multi-modal_convnext-roberta-base_vldoc-embedding'),
    Tasks.license_plate_detection:
    (Pipelines.license_plate_detection,
     'damo/cv_resnet18_license-plate-detection_damo'),
    Tasks.fill_mask: (Pipelines.fill_mask, 'damo/nlp_veco_fill-mask-large'),
    Tasks.feature_extraction: (Pipelines.feature_extraction,
                               'damo/pert_feature-extraction_base-test'),
    Tasks.action_recognition: (Pipelines.action_recognition,
                               'damo/cv_TAdaConv_action-recognition'),
    Tasks.action_detection: (Pipelines.action_detection,
                             'damo/cv_ResNetC3D_action-detection_detection2d'),
    Tasks.live_category: (Pipelines.live_category,
                          'damo/cv_resnet50_live-category'),
    Tasks.video_category: (Pipelines.video_category,
                           'damo/cv_resnet50_video-category'),
    Tasks.multi_modal_embedding: (Pipelines.multi_modal_embedding,
                                  'damo/multi-modal_clip-vit-base-patch16_zh'),
    Tasks.generative_multi_modal_embedding:
    (Pipelines.generative_multi_modal_embedding,
     'damo/multi-modal_gemm-vit-large-patch14_generative-multi-modal-embedding'
     ),
    Tasks.multi_modal_similarity:
    (Pipelines.multi_modal_similarity,
     'damo/multi-modal_team-vit-large-patch14_multi-modal-similarity'),
    Tasks.visual_question_answering:
    (Pipelines.visual_question_answering,
     'damo/mplug_visual-question-answering_coco_large_en'),
    Tasks.video_question_answering:
    (Pipelines.video_question_answering,
     'damo/multi-modal_hitea_video-question-answering_base_en'),
    Tasks.video_embedding: (Pipelines.cmdssl_video_embedding,
                            'damo/cv_r2p1d_video_embedding'),
    Tasks.text_to_image_synthesis:
    (Pipelines.text_to_image_synthesis,
     'damo/cv_diffusion_text-to-image-synthesis_tiny'),
    Tasks.text_to_video_synthesis: (Pipelines.text_to_video_synthesis,
                                    'damo/text-to-video-synthesis'),
    Tasks.body_2d_keypoints: (Pipelines.body_2d_keypoints,
                              'damo/cv_hrnetv2w32_body-2d-keypoints_image'),
    Tasks.body_3d_keypoints: (Pipelines.body_3d_keypoints,
                              'damo/cv_canonical_body-3d-keypoints_video'),
    Tasks.hand_2d_keypoints:
    (Pipelines.hand_2d_keypoints,
     'damo/cv_hrnetw18_hand-pose-keypoints_coco-wholebody'),
    Tasks.card_detection: (Pipelines.card_detection,
                           'damo/cv_resnet_carddetection_scrfd34gkps'),
    Tasks.content_check: (Pipelines.content_check,
                          'damo/cv_resnet50_content-check_cc'),
    Tasks.face_detection:
    (Pipelines.mog_face_detection,
     'damo/cv_resnet101_face-detection_cvpr22papermogface'),
    Tasks.face_liveness: (Pipelines.face_liveness_ir,
                          'damo/cv_manual_face-liveness_flir'),
    Tasks.face_recognition: (Pipelines.face_recognition,
                             'damo/cv_ir101_facerecognition_cfglint'),
    Tasks.facial_expression_recognition:
    (Pipelines.facial_expression_recognition,
     'damo/cv_vgg19_facial-expression-recognition_fer'),
    Tasks.face_attribute_recognition:
    (Pipelines.face_attribute_recognition,
     'damo/cv_resnet34_face-attribute-recognition_fairface'),
    Tasks.face_2d_keypoints: (Pipelines.face_2d_keypoints,
                              'damo/cv_mobilenet_face-2d-keypoints_alignment'),
    Tasks.face_quality_assessment:
    (Pipelines.face_quality_assessment,
     'damo/cv_manual_face-quality-assessment_fqa'),
    Tasks.video_multi_modal_embedding:
    (Pipelines.video_multi_modal_embedding,
     'damo/multi_modal_clip_vtretrival_msrvtt_53'),
    Tasks.image_color_enhancement:
    (Pipelines.image_color_enhance,
     'damo/cv_csrnet_image-color-enhance-models'),
    Tasks.virtual_try_on: (Pipelines.virtual_try_on,
                           'damo/cv_daflow_virtual-try-on_base'),
    Tasks.image_colorization: (Pipelines.ddcolor_image_colorization,
                               'damo/cv_ddcolor_image-colorization'),
    Tasks.video_colorization: (Pipelines.video_colorization,
                               'damo/cv_unet_video-colorization'),
    Tasks.image_segmentation:
    (Pipelines.image_instance_segmentation,
     'damo/cv_swin-b_image-instance-segmentation_coco'),
    Tasks.image_driving_perception:
    (Pipelines.yolopv2_image_driving_percetion_bdd100k,
     'damo/cv_yolopv2_image-driving-perception_bdd100k'),
    Tasks.image_depth_estimation:
    (Pipelines.image_depth_estimation,
     'damo/cv_newcrfs_image-depth-estimation_indoor'),
    Tasks.indoor_layout_estimation:
    (Pipelines.indoor_layout_estimation,
     'damo/cv_panovit_indoor-layout-estimation'),
    Tasks.video_depth_estimation:
    (Pipelines.video_depth_estimation,
     'damo/cv_dro-resnet18_video-depth-estimation_indoor'),
    Tasks.panorama_depth_estimation:
    (Pipelines.panorama_depth_estimation,
     'damo/cv_unifuse_panorama-depth-estimation'),
    Tasks.image_style_transfer: (Pipelines.image_style_transfer,
                                 'damo/cv_aams_style-transfer_damo'),
    Tasks.face_image_generation: (Pipelines.face_image_generation,
                                  'damo/cv_gan_face-image-generation'),
    Tasks.image_super_resolution: (Pipelines.image_super_resolution,
                                   'damo/cv_rrdb_image-super-resolution'),
    Tasks.image_debanding: (Pipelines.image_debanding,
                            'damo/cv_rrdb_image-debanding'),
    Tasks.image_portrait_enhancement:
    (Pipelines.image_portrait_enhancement,
     'damo/cv_gpen_image-portrait-enhancement'),
    Tasks.product_retrieval_embedding:
    (Pipelines.product_retrieval_embedding,
     'damo/cv_resnet50_product-bag-embedding-models'),
    Tasks.image_to_image_generation:
    (Pipelines.image_to_image_generation,
     'damo/cv_latent_diffusion_image2image_generate'),
    Tasks.image_classification:
    (Pipelines.daily_image_classification,
     'damo/cv_vit-base_image-classification_Dailylife-labels'),
    Tasks.image_object_detection:
    (Pipelines.image_object_detection_auto,
     'damo/cv_yolox_image-object-detection-auto'),
    Tasks.ocr_recognition:
    (Pipelines.ocr_recognition,
     'damo/cv_convnextTiny_ocr-recognition-general_damo'),
    Tasks.skin_retouching: (Pipelines.skin_retouching,
                            'damo/cv_unet_skin-retouching'),
    Tasks.faq_question_answering:
    (Pipelines.faq_question_answering,
     'damo/nlp_structbert_faq-question-answering_chinese-base'),
    Tasks.crowd_counting: (Pipelines.crowd_counting,
                           'damo/cv_hrnet_crowd-counting_dcanet'),
    Tasks.video_single_object_tracking: (
        Pipelines.video_single_object_tracking,
        'damo/cv_vitb_video-single-object-tracking_ostrack'),
    Tasks.image_reid_person: (Pipelines.image_reid_person,
                              'damo/cv_passvitb_image-reid-person_market'),
    Tasks.text_driven_segmentation: (
        Pipelines.text_driven_segmentation,
        'damo/cv_vitl16_segmentation_text-driven-seg'),
    Tasks.movie_scene_segmentation: (
        Pipelines.movie_scene_segmentation,
        'damo/cv_resnet50-bert_video-scene-segmentation_movienet'),
    Tasks.shop_segmentation: (Pipelines.shop_segmentation,
                              'damo/cv_vitb16_segmentation_shop-seg'),
    Tasks.image_inpainting: (Pipelines.image_inpainting,
                             'damo/cv_fft_inpainting_lama'),
    Tasks.image_paintbyexample: (Pipelines.image_paintbyexample,
                                 'damo/cv_stable-diffusion_paint-by-example'),
    Tasks.controllable_image_generation:
    (Pipelines.controllable_image_generation,
     'dienstag/cv_controlnet_controllable-image-generation_nine-annotators'),
    Tasks.video_inpainting: (Pipelines.video_inpainting,
                             'damo/cv_video-inpainting'),
    Tasks.video_human_matting: (Pipelines.video_human_matting,
                                'damo/cv_effnetv2_video-human-matting'),
    Tasks.human_reconstruction: (Pipelines.human_reconstruction,
                                 'damo/cv_hrnet_image-human-reconstruction'),
    Tasks.video_frame_interpolation: (
        Pipelines.video_frame_interpolation,
        'damo/cv_raft_video-frame-interpolation'),
    Tasks.video_deinterlace: (Pipelines.video_deinterlace,
                              'damo/cv_unet_video-deinterlace'),
    Tasks.human_wholebody_keypoint: (
        Pipelines.human_wholebody_keypoint,
        'damo/cv_hrnetw48_human-wholebody-keypoint_image'),
    Tasks.hand_static: (Pipelines.hand_static,
                        'damo/cv_mobileface_hand-static'),
    Tasks.face_human_hand_detection: (
        Pipelines.face_human_hand_detection,
        'damo/cv_nanodet_face-human-hand-detection'),
    Tasks.face_emotion: (Pipelines.face_emotion, 'damo/cv_face-emotion'),
    Tasks.product_segmentation: (Pipelines.product_segmentation,
                                 'damo/cv_F3Net_product-segmentation'),
    Tasks.referring_video_object_segmentation: (
        Pipelines.referring_video_object_segmentation,
        'damo/cv_swin-t_referring_video-object-segmentation'),
    Tasks.video_summarization: (Pipelines.video_summarization,
                                'damo/cv_googlenet_pgl-video-summarization'),
    Tasks.image_skychange: (Pipelines.image_skychange,
                            'damo/cv_hrnetocr_skychange'),
    Tasks.translation_evaluation: (
        Pipelines.translation_evaluation,
        'damo/nlp_unite_mup_translation_evaluation_multilingual_large'),
    Tasks.video_object_segmentation: (
        Pipelines.video_object_segmentation,
        'damo/cv_rdevos_video-object-segmentation'),
    Tasks.video_multi_object_tracking: (
        Pipelines.video_multi_object_tracking,
        'damo/cv_yolov5_video-multi-object-tracking_fairmot'),
    Tasks.image_multi_view_depth_estimation: (
        Pipelines.image_multi_view_depth_estimation,
        'damo/cv_casmvs_multi-view-depth-estimation_general'),
    Tasks.image_fewshot_detection: (
        Pipelines.image_fewshot_detection,
        'damo/cv_resnet101_detection_fewshot-defrcn'),
    Tasks.image_body_reshaping: (Pipelines.image_body_reshaping,
                                 'damo/cv_flow-based-body-reshaping_damo'),
    Tasks.image_face_fusion: (Pipelines.image_face_fusion,
                              'damo/cv_unet-image-face-fusion_damo'),
    Tasks.image_matching: (
        Pipelines.image_matching,
        'damo/cv_quadtree_attention_image-matching_outdoor'),
    Tasks.image_quality_assessment_mos: (
        Pipelines.image_quality_assessment_mos,
        'damo/cv_resnet_image-quality-assessment-mos_youtubeUGC'),
    Tasks.image_quality_assessment_degradation: (
        Pipelines.image_quality_assessment_degradation,
        'damo/cv_resnet50_image-quality-assessment_degradation'),
    Tasks.vision_efficient_tuning: (
        Pipelines.vision_efficient_tuning,
        'damo/cv_vitb16_classification_vision-efficient-tuning-adapter'),
    Tasks.object_detection_3d: (Pipelines.object_detection_3d_depe,
                                'damo/cv_object-detection-3d_depe'),
    Tasks.bad_image_detecting: (Pipelines.bad_image_detecting,
                                'damo/cv_mobilenet-v2_bad-image-detecting'),
    Tasks.nerf_recon_acc: (Pipelines.nerf_recon_acc,
                           'damo/cv_nerf-3d-reconstruction-accelerate_damo'),
    Tasks.siamese_uie: (Pipelines.siamese_uie,
                        'damo/nlp_structbert_siamese-uie_chinese-base'),
    Tasks.pedestrian_attribute_recognition: (
        Pipelines.pedestrian_attribute_recognition,
        'damo/cv_resnet50_pedestrian-attribute-recognition_image'),
}
