Round 3 已完成，三份状态 YAML 均解析通过，前三轮历史和所有旧版本均保留。

分支动作：

- `frozen_definition_county_causal_effect`：`abandon`
- `randomized_invitation_access_margin`：`fork`，成为当前活动分支
- 第二轮的 `backtrack` 与 `continue` 记录未被覆盖

最深受影响层级：

- **势（制度与具体情境）**，并造成下游的**术（识别设计）**失效。
- 县级进入依据预期 2024 年高需求和供应退出进行选择；4 个处理县已有年中门诊关闭计划；控制县没有联合支持；也不存在门槛、抽签或其他可信外生规则。
- 这不要求否定可及性问题或其微观机制，但县级比较已无法承担因果识别。

保留的知识：

- 冻结口径下农村增长 8%、城市增长 3%、描述性差异 5 个百分点。
- 编码修正、2021–2023 年趋势重建和选择制度档案仍有效。
- 平行预趋势无法抵消已知的 2024 年需求与供应选择。
- 随机邀请是独立、狭窄的实验性证据，不能识别县级进入效应。

放弃的内容：

- `C3-v3`：利用当前县级比较识别平台进入的县级因果效应，状态为 `abandoned`。
- 明确禁止使用无共同支持的控制、匹配、加权或合成组合继续“修复”。
- 只有真正新增的共同支持或独立于预期需求和供应退出的外生县级变异才能重启。

分叉的内容：

- 2,400 名预登记、高旅行障碍且有临床随访需要居民中的随机邀请效应。
- 研究对象限于平台前三个月、预约稀缺条件下的邀请分配，不等于实际接受治疗、全县居民、县级平台进入或福利效应。

新增/更新主张：

- `C3-v3`：县级进入因果效应——`abandoned`
- `C4-v3`：全县有效可及性改善——`underidentified`
- `C5-v2`：全县居民福利改善——`underidentified`
- `C6-v1`：随机邀请使 30 日内完成指征性随访提高 15 个百分点——`supported`，仅指实际随机分配制度下的窄 ITT 对比
- `C7-v1`：随机邀请使往返旅行时间减少 90 分钟——`provisional`，仍需审计测量、缺失和区间
- `C8-v1`：90 日健康、总医疗支出和诊所退出未测得变化——`provisional`，不能解释为等效或零效应
- `C9-v1`：实验人群的有效可及性改善——`provisional`，共享医生造成的挤出尚未排除

下一项区分性检验：

将邀请分配与预约名额、医生名册和负荷，以及受邀者、未受邀者和其他患者的随访完成情况连接；按真实随机化方案用随机化推断复算 ITT，审计旅行时间和置信区间，并构造医生层面的暴露/饱和度。检验受邀者收益是否伴随同一医生其他患者的延期或损失：

- 总指征性随访上升且无抵消损失：支持该实验人群的“可及性扩张”；
- 收益由他人损失抵消：回溯到“稀缺容量重新配给”机制。

更新文件：

- [RESEARCH_MAINLINE.yaml](C:/Users/ENAN/AppData/Local/Temp/junzi-economist-mainline-x015/RESEARCH_MAINLINE.yaml)
- [CLAIM_LEDGER.yaml](C:/Users/ENAN/AppData/Local/Temp/junzi-economist-mainline-x015/CLAIM_LEDGER.yaml)
- [BRANCH_LOG.yaml](C:/Users/ENAN/AppData/Local/Temp/junzi-economist-mainline-x015/BRANCH_LOG.yaml)
- [DECISION_NOTE.md](C:/Users/ENAN/AppData/Local/Temp/junzi-economist-mainline-x015/DECISION_NOTE.md)
