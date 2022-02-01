# -*- coding: utf-8 -*-
__author__ = "Sommily"

import os
import json
import pandas

EXCEL_TEMPLATE_HEADER = ["所属章", "类型", "题干", "分值", "难度", "关联知识点", "解析", "题目中包含 LaTeX 公式", "正确答案", "选项A", "选项B", "选项C",
                         "选项D", "选项E", "选项F", "选项G", "选项H", "选项I", "选项J", "选项K", "选项L", "选项M", "选项N", "选项O"]


def load_exam_json(folder_path: str, merge_all=True):
    error_topic_list = []
    all_df = pandas.DataFrame(columns=EXCEL_TEMPLATE_HEADER, index=[])
    j = 0
    for file_name in os.listdir(folder_path):
        if not file_name.endswith(".json") or file_name == "error_topic.json":
            continue

        df = pandas.DataFrame(columns=EXCEL_TEMPLATE_HEADER, index=[])
        with open(os.path.join(folder_path, file_name), 'r') as f:
            data = json.load(f)
            topic_list = data.get("list").get("examDtoList")
            exam_name = file_name.rstrip(".json")
            print(f"{exam_name}: {len(topic_list)}")
            for i, topic in enumerate(topic_list):
                topic_type = str(topic.get("examTypeName")).strip("题")
                if topic_type == "不定项选择":
                    topic_type = "多选"
                if topic_type == "判断题AB":
                    topic_type = "判断题"
                content = topic.get("content").strip("\n ")
                content = content.replace("<br>", "")
                content = content.replace("<br />", "")
                content = content.replace("&emsp;", "")
                content = content.replace("&nbsp;", "")
                score = int(topic.get("scoreRules").get("ruleScore") * 10)
                if score > 10:
                    score = 10
                difficulty = "简单"
                knowLedgeName = ";".join(
                    list(
                        map(
                            lambda
                                x: f"{x.get('parentChapterName')}-{x.get('chapterName')}-{x.get('knowLedgeName')}({x.get('yaoQiuName')})",
                            topic.get("knowledge")
                        )
                    )
                )
                analysis = topic.get("analysis").strip("\n ")
                analysis = analysis.replace("<br>", "")
                analysis = analysis.replace("<br />", "")
                analysis = analysis.replace("&emsp;", "")
                analysis = analysis.replace("&nbsp;", "")

                include_LaTex = "否"
                if topic.get("examType") == 4:
                    answer = ("A", "B")[topic.get("answer") == '0']
                    option_a = "对"
                    option_b = "错"
                    option_c = ""
                    option_d = ""
                elif topic.get("examType") == 11:
                    answer = topic.get("answer").replace(",", "")
                    option_a = "对"
                    option_b = "错"
                    option_c = ""
                    option_d = ""
                else:
                    answer = topic.get("answer").replace(",", "")
                    if len(topic.get("optionList")) == 0:
                        option_a = "正确答案"
                        option_b = "正确答案"
                        option_c = "错误答案"
                        option_d = "正确答案"
                    else:
                        option_a = topic.get("optionList")[0]
                        option_b = topic.get("optionList")[1]
                        option_c = topic.get("optionList")[2]
                        option_d = topic.get("optionList")[3]

                option_a = option_a.replace("①", "1")
                option_a = option_a.replace("②", "2")
                option_a = option_a.replace("③", "3")
                option_a = option_a.replace("④", "4")

                option_b = option_b.replace("①", "1")
                option_b = option_b.replace("②", "2")
                option_b = option_b.replace("③", "3")
                option_b = option_b.replace("④", "4")

                option_c = option_c.replace("①", "1")
                option_c = option_c.replace("②", "2")
                option_c = option_c.replace("③", "3")
                option_c = option_c.replace("④", "4")

                option_d = option_d.replace("①", "1")
                option_d = option_d.replace("②", "2")
                option_d = option_d.replace("③", "3")
                option_d = option_d.replace("④", "4")

                df.loc[i] = [exam_name, topic_type, content, score, difficulty, knowLedgeName, analysis, include_LaTex,
                             answer, option_a, option_b, option_c, option_d, None, None, None, None, None, None, None,
                             None, None, None, None]
                if merge_all:
                    all_df.loc[j] = [exam_name, topic_type, content, score, difficulty, knowLedgeName, analysis,
                                     include_LaTex, answer, option_a, option_b, option_c, option_d, None, None, None,
                                     None, None, None, None, None, None, None, None]
                j += 1
                if "233" in content or "233" in analysis:
                    error_topic_list.append(content)

        export_file_name = "".join([folder_path, exam_name, ".xlsx"])
        df.to_excel(export_file_name, sheet_name="题库模板", index=None)

    if merge_all:
        all_df.to_excel("./all.xlsx", sheet_name="题库模板", index=None)
    json.dump(error_topic_list, open(folder_path + "/error_topic.json", 'w'))


if __name__ == "__main__":
    # load_exam_json(folder_path="/Users/Sommily/workspace/Scrapy233Exam/期货从业/基础知识/真题")
    # load_exam_json(folder_path="/Users/Sommily/workspace/Scrapy233Exam/期货从业/基础知识/模拟试题")
    # load_exam_json(folder_path="/Users/Sommily/workspace/Scrapy233Exam/期货从业/基础知识/章节练习")

    # load_exam_json(folder_path="/Users/Sommily/workspace/Scrapy233Exam/期货从业/法律法规/真题")
    # load_exam_json(folder_path="/Users/Sommily/workspace/Scrapy233Exam/期货从业/法律法规/模拟试题")
    # load_exam_json(folder_path="/Users/Sommily/workspace/Scrapy233Exam/期货从业/法律法规/章节练习")
    pass
