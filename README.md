
# DevOps

这是我的个人 DevOps / SRE 学习与实践作品集，涵盖了从 **容器化 → K8s 部署 → CI/CD → 监控 → IaC → GitOps** 的完整流程。

博客链接：http://117.72.175.93:30080/，账号密码可以注册

Grafana 链接：http://120.55.57.128:3000
账号：admin，密码：123qwe123???
在Dashboards中查看监控面板

## 仓库结构
- `django/`：Django 示例应用，支持 Docker 打包镜像后用 Docker/K8s 部署
- `k8s/`：通过 K8S 集群部署 Django、MySQL、Redis 的配置文件
- `monitoring/`：Prometheus + Grafana 监控 MySQL、Redis 指标配置文件
- `custom_exporter/`：自定义 Python Exporter，采集自定义指标（待实现）
- `ci_cd/`：Jenkins Pipeline、Ansible 自动化 （待实现）
- `lac/`：Terraform + Ansible 管理资源（待实现）
- `docs/`：学习笔记和面试总结（待完善）

## 项目亮点
- **云原生全链路**：从应用开发到上线监控，完整 DevOps 实践
- **可观测性**：监控 MySQL/Redis 应用，Grafana 仪表盘展示
- **自动化**：Jenkins/Github Actions 实现 CI/CD 流水线
- **IaC**：Terraform 管理云资源，Ansible 管理配置

## 技术栈
Python, Django, Docker, Kubernetes, Jenkins, Ansible, Prometheus, Grafana, Terraform

