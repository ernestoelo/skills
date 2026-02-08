# \<Project Name>

## Overview

### System Description

Briefly describe:

- What this system is
- What problem it solves
- Who it is for

---

### Architecture Overview

| Overview | Architecture |
|---------|--------------|
| ![doc/system-overview.png](../diagrams/templates/system-overview.png) doc/system-overview.png | ![doc/system-architecture.png](../diagrams/templates/system-architecture.png) doc/system-architecture.png |

---

### System Context

Describe how this system fits into the overall ecosystem:

- Backend components
- Frontend / Mobile clients
- External services
- Hardware / ROS / APIs (if applicable)

If this repository represents a component, highlight it in a context diagram.

---

## Setup

All setup steps must be script-based.

### Clone Repository

```sh
git clone <repository-url>
```

### Configuration and Prerequisites

```sh
cd scripts
bash setup_config.sh
bash install_prerequisites.sh
bash setup_environment.sh
```

---

## Production Environment

### Production Architecture

![doc/system-prod-env.png](../diagrams/templates/system-prod-env.png)

doc/system-prod-env.png

---

### Install Production Services

```sh
cd scripts
bash install_prod_server.sh
```

---

### Running Services and Logs

Describe how to check:

- Service status
- Application logs
- Web server logs

Example:

```sh
sudo journalctl -fu <service>
sudo tail -f /var/log/<service>/<logfile>.log
```

---

### Deployment

```sh
bash deploy_prod_server.sh
```

---

### Restart Services

```sh
bash restart_prod_server.sh
```

---

### Uninstall

```sh
bash uninstall_prod_server.sh
```

---

## Development Environment

```sh
cd scripts
bash run_dev_server.sh
```

---

## Useful Scripts

| Script | Environment | Description |
|------|------------|-------------|
| install_prod_server.sh | Production | Install production services |
| deploy_prod_server.sh | Production | Deploy new version |
| restart_prod_server.sh | Production | Restart services |
| run_dev_server.sh | Development | Run development server |

---

## General Notes

- All critical operations must be scripted
- README must reflect reality
- Undocumented behavior is considered non-existent