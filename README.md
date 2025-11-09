# RORO 🎸
> 최고의 인디 가수 '한로로(Han Roro)'의 인기를 추적하고 계산하는 프로젝트

[![GitHub Stars](https://img.shields.io/github/stars/Gyupil/RORO?style=for-the-badge)](https://github.com/Gyupil/RORO/stargazers)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)


'RORO'는 데이터를 기반으로 나날이 증가하는 한로로의 인기를 분석하고 시각화하는 것을 목표로 합니다.

![RORO Project Demo](https://github.com/user-attachments/assets/6ea36599-a6bc-4c8d-8028-3fb864909b07)

---

## ✨ 주요 기능

* **📈 데이터 크롤링:** Spotify, 네이버 데이터랩, 멜론 등 다양한 플랫폼에서 '한로로' 관련 데이터를 주기적으로 수집합니다.
* **🧮 'RORO 인덱스' 계산:** 수집된 데이터를 기반으로 독자적인 'RORO 인덱스'를 계산하여 인기도를 수치화합니다.
* **📊 데이터 시각화:** 단일 페이지 웹 대시보드(HTML)를 통해 계산된 인덱스 변화 추이를 직관적으로 보여줍니다.
* **🤖 자동화 스케줄링:** 스케줄러가 정해진 시간마다 자동으로 데이터를 수집하고 'RORO 인덱스'를 갱신합니다.

---

## 🛠️ 기술 스택

| 구분 | 기술 |
| :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) (Production) / ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) (Local) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) |
| **Deployment** | ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white) |

---

## ☁️ 배포

이 서비스는 **[Render.com](https://render.com/)**의 Web Service와 Managed PostgreSQL을 통해 배포되었습니다.

* **배포 URL:** `https://roro-3kk8.onrender.com` (이 부분은 실제 Render URL로 수정해 주세요)

---
