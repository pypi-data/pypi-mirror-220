import os
# from loguru import logger
# import sys
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s | %(message)s")

modelHeader = """
from pydantic import BaseModel
from typing import *

# 可自行修改增加校验精准度

"""
BASERUNPARAM = """
class BASE_RUN_PARAM(BaseModel):
    timeOut: int = None
"""
MODEL_INFO = """
class {{ className }}(BaseModel):
    {% if args %}
    {% for argName, argType in args %}
    {{ argName }}: {{ argType }}
    {% endfor %}
    {% else %}
    ...
    {% endif %}
"""

ACTION_INFO = """
from SDK.run_define import Actions
from SDK.base import *

from .models import {{ adapMdl }}, {{ inputModel }}, {{ outputModel }}, BASE_RUN_PARAM


class {{ actionsName }}(Actions):

    def __init__(self):
        # 初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.baseRunModel = BASE_RUN_PARAM
        self.outputModel = {{ outputModel }}
        self.adapMdl = {{ adapMdl }}


    def adapter(self, data={}):
        # write your code
        ...    
    
    
    def run(self, params={}):
        # write your code
        ...

"""
FAST_API_INFO = """
from actions import *
from fastapi import FastAPI,HTTPException
import os
import uvicorn
import typing
import json
from SDK.base import * 

desc = \
'''
  欢迎使用 1.0.0 版本SDK提供的FastAPI调试接口。\n
  
  Love it!  -- MVTECH

'''
test_server = FastAPI(title="MVTECH-Plugin Test Server", version="1.0.0", description=desc)
{% for name, className in init_list %}
@test_server.post("/actions/{{ name }}",response_model={{ className }}().outputModel,tags=["动作"])
def action_{{ name }}(action_name:str="{{ name }}",
                      adapter_data:{{ className }}().adapMdl=None,
                      baseRunModel:{{ className }}().baseRunModel=None,
                      input_data:{{ className }}().inputModel=None):
    
    clearLog()

    adapter_data = adapter_data.dict()

    baseRunModel = baseRunModel.dict()

    input_data = input_data.dict()

    output = {{ className }}()._run(input_data,adapter_data,baseRunModel)

    if output["body"].get("error_trace"):
        raise HTTPException(500,detail=output["body"]["error_trace"])
    else:
        output_data = output["body"]["output"]

    return output_data
{% endfor %}

  
def runserver():
    os.system("")
    log("attention","在浏览器内输入 http://127.0.0.1:7007/docs# 以进行接口测试")
    log("attention","在浏览器内输入 http://127.0.0.1:7007/redoc 以查看帮助文档")
    uvicorn.run(test_server,host="127.0.0.1", port=7007)

if __name__ == '__main__':

    runserver()
"""

TRIGGER_INFO = """
from SDK.run_define import Triggers
from SDK.base import *

from .models import {{ adapMdl }}, {{ inputModel }}, {{ outputModel }}


class {{ triggersName }}(Triggers):

    def __init__(self):
        # 初始化
        
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.adapMdl = {{ adapMdl }}


    def adapter(self, data={}):
        # write your code
        ...    

    def run(self, params={}):
        # write your code
        # 返回必须使用 self.send({})
        
        ...

"""

ACTION_FAST_API_INFO = """
{
	"version": "v1",
	"type": "action_start",
	"body": {
		"action": "{{ title }}",
		"meta": {},
		"adapter": {},
		"nextStep": null,
		"input_data": {}
	}
}

"""

TRIGGER_FAST_API_INFO = """
{
	"version": "v1",
	"type": "trigger_start",
	"body": {
		"trigger": "{{ title }}",
		"meta": {},
		"adapter": {},
		"nextStep": {
			"send_url": "http://127.0.0.1:8001/send",
			"jwt": ""
		},
		"input_data": {}
      "enable_web": false
	}
}

"""

MAIN_INFO = """#!/usr/bin/env python

from SDK.plugin import Plugin
from SDK.cli import client

{% if actionClassees %}
import actions
{% endif %}
{% if triggerClassees %}
import triggers
{% endif %}
{% if indicatorReceiverClassees %}
import indicator_receivers
{% endif %}
{% if alarmReceiverClassees %}
import alarm_receivers
{% endif %}


# 整个程序入口


class {{ pluginName }}(Plugin):

    def __init__(self):
        super().__init__()
        
        {% for actionClass in actionClassees %}
        self.add_actions(actions.{{ actionClass }}())
        {% endfor %}

        {% for triggerClass in triggerClassees %}
        self.add_triggers(triggers.{{ triggerClass }}())
        {% endfor %}

        {% for indicatorReceiverClasse in indicatorReceiverClassees %}
        self.add_indicator_receivers(indicator_receivers.{{ indicatorReceiverClasse }}())
        {% endfor %}
        
        {% for alarmReceiverClasse in alarmReceiverClassees %}
        self.add_alarm_receivers(alarm_receivers.{{ alarmReceiverClasse }}())
        {% endfor %}


def main():

    client({{ pluginName }}())



if __name__ == '__main__':

    main()
    
"""

INIT_INFO = """
{% for name, className in init_list %}
from .{{ name }} import {{ className }}
{% endfor %}
"""

HELP_INFO = """
# {{ name }}

## About
{{ name }}



## adapter

{% if adapter %}


{% for field_name, field_data in adapter.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|

{%- endfor %}


{% endif %}


## Actions

{% if actions %}

{% for action, actionData in actions.items() %}

### {{ action }}

---

{% for action_name,action_data in actionData.items() %}

{% if action_name == 'input' %}
#### Input

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if action_name == 'output' %}
#### Output

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Triggers

---

{% if triggers %}


{% for trigger, triggerData in triggers.items() %}

### {{ trigger }}

---

{% for trigger_name,trigger_data in triggerData.items() %}

{% if trigger_name == 'input' %}
#### Input

{% for field_name, field_data in trigger_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if action_name == 'output' %}
#### Output

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}


## Types

{% if types %}

{% for type_name, type_data in types.items() %}

### {{ type_name }}

{% for field_name, field_data in type_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|

{%- endfor %}

{% endfor %}

{% endif %}


## 版本信息
- {{ version }}

## 参考引用
"""
