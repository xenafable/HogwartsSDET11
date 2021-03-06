import pytest
from test_requests.test_wework.api.base_api import BaseApi
from test_requests.test_wework.api.corp_tag import CorpTag


class TestCorpTag():
    test_data = BaseApi.yaml_load('test_requests/test_wework/testcase/test_corptag.data.yml')
    test_steps = BaseApi.yaml_load('test_requests/test_wework/testcase/test_corptag.step.yml')

    @classmethod
    def setup_class(cls):
        # TODO： 删除测试数据，将需要数据封装

        cls.corptag = CorpTag()

        # 清除数据
        cls.corptag.get()
        for name in cls.test_data['test_add']:
            x = cls.corptag.jsonpath("$..tag[?(@.name=='{}')]".format(name))
            if x:
                cls.corptag.delete(tag_id=[x[0]['id']])

    def test_get_api_corp_tag(self):

        r = self.corptag.get()

        print(r)

        assert r['errcode'] == 0

    # def test_get_corp_tag(self):
    #     body = {
    #         "tag_id": [
    #             "etXXXXXXXXXX",
    #             "etYYYYYYYYYY"
    #         ]
    #     }
    #     r = self.corptag.get()

    #     print(r)

    #     assert r['errcode'] == 0

    # def test_add_corp_tag(self):
    #     # tag.name required
    #     body = {
    #         "group_id": "eta5cUCgAARJtCoUzDTc2CtbCc_avCXQ",
    #         # "group_name": "GROUP_NAME",
    #         # "order": 1,
    #         "tag": [{
    #                 "name": "TAG_NAME_1",
    #                 # "order": 1
    #             },
    #             # {
    #             #     "name": "TAG_NAME_2",
    #             #     "order": 2
    #             # }
    #         ]
    #     }
    #     r = self.corptag.add(body)

    #     print(r)

    #     assert r['errcode'] == 0

    def test_add_corp_tag(self):
        # tag.name required
        name = "TAG_NAME_2"
        r = self.corptag.add(name)

        print(r)

        assert r['errcode'] == 0

    def test_edit_corp_tag(self):
        # tag.name required
        body = {
            "id": "eta5cUCgAAYVSsXdp5uFvbbim6ktAzhQ", # required
            "name": "NEW_TAG_NAME",
            "order": 1
        }
        r = self.corptag.edit(body)

        print(r)

        assert r['errcode'] == 0

    # @pytest.mark.parametrize('name', [
    #     'demo1', '中文测试', '*', '', '123'
    # ])
    @pytest.mark.parametrize('name', test_data['test_delete'])
    def test_delete_corp_tag(self, name):
        # name = "TAG_NAME_1"
        tags_path = '$..tag[?(@.name != "")]'
        find_tag_path = '$..tag[?(@.name=="{}")]'.format(name)

        print(find_tag_path)

        # add_body = {
        #     "group_id": "eta5cUCgAARJtCoUzDTc2CtbCc_avCXQ",
        #     "tag": [{
        #             "name": name
        #         }
        #     ]
        # }
        # 获取原始数据
        source_tags = self.corptag.get()

        # 删除测试标签
        exist_name = self.corptag.jsonpath(source_tags, find_tag_path)
        if exist_name:
            self.corptag.delete({
                "tag_id": [
                    exist_name[0]['id']
                ]
            })

        # 环境清理后开始测试
        source_tags = self.corptag.get()
        source_tags_size = len(self.corptag.jsonpath(source_tags, tags_path))
        print(source_tags_size)

        # 添加tag
        self.corptag.add(name)
        add_tags = self.corptag.get()
        print(add_tags)
        assert len(self.corptag.jsonpath(add_tags, tags_path)) == (source_tags_size + 1)

        # 取得添加tag的id
        result = self.corptag.jsonpath(add_tags, find_tag_path)
        print(result)

        # 删除tag
        # delete_body = {
        #     "tag_id": [
        #         result[0]['id']
        #     ]
        # }
        tag_id = result[0]['id']
        r = self.corptag.delete(tag_id)

        # 断言
        print(r)
        assert r['errcode'] == 0

    @pytest.mark.parametrize('name', test_data['test_delete'])
    def test_delete_step(self, name):
        self.corptag._params['name'] = name
        self.corptag.steps_run(self.test_steps['test_delete'])

    @pytest.mark.parametrize('name', test_data['test_add'])
    def test_add_step(self, name):
        self.corptag._params['name'] = name
        self.corptag.steps_run(self.test_steps['test_add'])

    def test_decorator(self):

        self.corptag.decorator()

    @classmethod
    def teardown_class(cls):
        # teardown清空数据风险比较大，因为一些异常强制退出执行case（如直接kill），会导致走不到teardown
        pass
