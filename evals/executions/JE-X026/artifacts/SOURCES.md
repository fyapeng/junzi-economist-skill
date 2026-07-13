# JE-X026 来源矩阵与检索记录

检索时点：2026-07-13（截至 11:34 Asia/Shanghai）。所有当前事实均优先核验官方或原始页面；网页与所链接文件分别记时。

## 已核验来源矩阵

| 来源 | 首次 issue / 文件日期 | 生效日期 | 网页发布日期 | 当前修订状态 | 本轮确切 artifact | 核验状态 | 可支持 | 不可支持 |
|---|---|---|---|---|---|---|---|---|
| Singh & Venkataramani, *Rationing by Race*, NBER WP 30380 | Issue: Aug 2022；历史版本页列首版 2022-08-17 | 不适用 | 落地页未另列网页发布日期 | 当前 PDF：Revised April 2026；实时 HTML：`2026-04-14` / April 2026；旧搜索缓存仍见 May 2024，冲突已保留 | [NBER landing page](https://www.nber.org/papers/w30380)；[current PDF](https://www.nber.org/system/files/working_papers/w30380/w30380.pdf)；DOI [10.3386/w30380](https://doi.org/10.3386/w30380) | `full-text-verified` | 当前版本的研究对象、样本与作者报告的结果/机制 | 中国/NHS 政策的赋值、推广与识别；独立验证所有因果假设 |
| 国家卫健委办公厅、国家中医药局综合司、国家疾控局综合司，国卫办医政发〔2024〕21号 | 正文落款 2024-10-28 | 正文未列统一生效日 | 2024-11-27 | 未见公开版本史或修订说明；不能据此断言无修订 | [官方正文](https://www.nhc.gov.cn/yzygj/c100068/202411/d85d3ba36c43460fa67deb333f52203b.shtml) | `official-text-verified` | 中央目标、职责、流程、知情同意、信息记录和目标期限 | 地方实际启用/合规、外生 rollout、阈值或可用比较组 |
| NHS England, “Diversion of referrals” | `unknown` | `unknown`；页面描述推广支持，不等于统一生效 | `unknown`；页面无显示日期 | `unknown`；无显示更新日或版本史 | [official webpage](https://www.england.nhs.uk/elective-care/best-practice-solutions/diversion-of-referrals/) | `official-text-verified` | capacity alert 的官方机制描述、红绿提示、患者选择节点、两处 early-adopter 汇总数字、推广意向 | early adopter 身份/日期/选择、阈值算法、外生推广、百分比的识别与不确定性 |

## 可变文件与哈希

| Artifact（2026-07-13 实际取得） | 大小/内容标记 | SHA-256 |
|---|---|---|
| `https://www.nber.org/system/files/working_papers/w30380/w30380.pdf` | 3,523,032 bytes；69 页；首页 `Revised April 2026` | `F1A5345821CDA6BF9DDC7D8B7E8D27341EB30F102D16B1DA00C34DCD667CCC85` |
| `https://www.nber.org/papers/w30380` HTML | 实时 HTML 标记 revision datetime `2026-04-14T12:00:00Z` | `3D90C1580C10D1707765F84CAEF74974B55A2AA347E89EC9381E3EF1E2F8FC1E` |
| `https://www.england.nhs.uk/elective-care/best-practice-solutions/diversion-of-referrals/` HTML | 页面无可见发布/更新日期 | `59A511495A3414D83CBCECC1C46B204EB47ECB4E02092D9973203F0F076974DC` |

两个 HTML 哈希对应 **2026-07-13T11:34:12+08:00 本轮保存的特定响应快照**。获取方式为 Windows PowerShell `Invoke-WebRequest` 的普通 `GET` 请求，没有设置认证、Cookie、条件请求、缓存控制或其他特殊请求头。动态网页可能因模板、脚本、分析标记、边缘节点或服务器生成内容变化而返回不同字节，后续请求不应被期待逐字节复现这两个 HTML 哈希。它们只用于标识本轮实际检查的网页响应；NBER 当前 PDF 的 SHA-256 才是本轮论文版本的稳定内容锚点。

NBER PDF 的 HTTP `Last-Modified: Wed, 08 Jul 2026 18:17:35 GMT` 只记录服务器对象变动，**不**作为论文修订日期；修订日期取自 PDF 首页和落地页显式版本字段。

国家卫健委页面对直接命令行下载返回 HTTP 412，本轮通过官方网页正文完整核验；未把重新序列化的检索文本冒充原始网页字节，因此不报告伪造的页面哈希。

## 查询与站点记录

本轮使用的核心查询/入口：

- `site:nber.org/papers "Rationing by Race" Singh Venkataramani`
- NBER DOI、工作论文落地页、当前 PDF 与历史版本链接；
- `site:nhc.gov.cn 国卫办医政发〔2024〕21号`
- `site:england.nhs.uk "Diversion of Referrals"`
- `site:england.nhs.uk "capacity alerts" "38 per cent"`
- NHS 页面所链接的 NHS Long Term Plan 仅作为页面自身所述背景；未用其年份填补当前页面缺失的发布日期。

## 日期审计

- NBER：issue、历史版本、当前修订、实时 HTML 版本字段、服务器 Last-Modified 和检索时间均分开。
- 国卫委：正文落款、网页发布日期、阶段目标期限与生效日期分开；生效日期缺失即记缺失。
- NHS：页面没有日期字段，故首次发布、生效、最近修订均记 `unknown`；不以网站版权、搜索引擎抓取日或 Long Term Plan 年份代替。
