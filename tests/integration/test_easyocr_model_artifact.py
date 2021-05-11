import pytest
import tempfile
import contextlib
import bentoml
from tests.bento_service_examples.easyocr_service import EasyOCRService
from bentoml.yatai.client import YataiClient

import easyocr

TEST_RESULT = ['西', '愚园路', '东', '315', '309', 'W', 'Yuyuan Rd。', 'E']

def test_easyocr_artifact_packs():
    svc = EasyOCRService()

    lang_list = ['ch_sim', 'en']
    recog_network = "zh_sim_g2"

    model = easyocr.Reader(lang_list=lang_list, gpu=False,
        download_enabled=True, recog_network=recog_network )   
    svc.pack('chinese_small', model, lang_list=lang_list, recog_network= recog_network)

    assert [x[1] for x in model.readtext("./chinese.jpg")] == 
     TEST_RESULT
    ), 'Run inference before saving the artifact'

    saved_path = svc.save()
    loaded_svc = bentoml.load(saved_path)
    
    assert [x[1] for x in loaded_svc.readtext("./chinese.jpg")] == 
     TEST_RESULT
    ),  'Run inference after saving the artifact'

    # clean up saved bundle
    yc = YataiClient()
    yc.repository.delete(f'{svc.name}:{svc.version}')
