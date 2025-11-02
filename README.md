# 📱 IMREALAPP

딥페이크 탐지·보호를 위한 **풀스택 미디어 처리 애플리케이션**
**Backend:** Django 5.1 + DRF · **Frontend:** React Native 0.73.9 (TypeScript)

---

## 🧭 개요

- **목적:** 이미지/영상에 대한 딥페이크 탐지, 보호(워터마크 등), 결과 리포트 및 이력 관리
- **구성:** Django REST API 백엔드 + React Native 모바일 앱
- **저장소 특징:** 동일 저장소에 Django(백엔드)와 React Native(프론트엔드) 공존

---

## 📂 프로젝트 구조

```
IMREALAPP/
├── BE/                          # Django 백엔드
│   ├── config/                  # Django 설정 (settings.py, urls.py)
│   ├── detection/               # 딥페이크 탐지
│   ├── protection/              # 미디어 보호(워터마크 등)
│   ├── reports/                 # 분석 리포트
│   ├── users/                   # 인증/사용자
│   ├── zoom/                    # Zoom 연동
│   ├── media_files/             # 미디어 파일 저장소
│   ├── manage.py
│   └── requirements.txt
│
├── FE/                          # React Native 프론트엔드 (실사용)
│   ├── src/
│   │   ├── screens/             # 화면 컴포넌트
│   │   │   ├── HomeScreen.tsx
│   │   │   ├── DetectScreen.tsx
│   │   │   ├── ProtectScreen.tsx
│   │   │   ├── WatermarkScreen.tsx
│   │   │   ├── HistoryScreen.tsx
│   │   │   └── NewsScreen.tsx
│   │   ├── components/          # 재사용 컴포넌트
│   │   ├── api/                 # apiClient.ts (백엔드 통신)
│   │   ├── types/               # 타입 정의
│   │   └── utils/               # 유틸 함수
│   ├── android/                 # Android 빌드 설정 (현재 이슈 발생)
│   ├── ios/                     # iOS 빌드 설정
│   ├── package.json
│   └── App.tsx
│
├── android/                     # 루트 레벨 RN(구성 유물, 0.82 계열)
├── ios/                         # 루트 레벨 RN(구성 유물)
├── App.tsx                      # 루트 레벨 RN(구성 유물)
├── package.json                 # 루트 레벨 RN(구성 유물)
└── README.md
```

---

## 🚨 중요: 이중 React Native 프로젝트 구조

현재 저장소에는 **두 개의 RN 프로젝트가 혼재**되어 있습니다.

| 구분    | 위치  | 버전/상태                | 비고                                   |
| ------- | ----- | ------------------------ | -------------------------------------- |
| 루트 RN | `/`   | React Native 0.82.x 흔적 | 과거 유물. 빌드 대상으로 사용하지 않음 |
| 실제 앱 | `/FE` | **React Native 0.73.9**  | **실제 실행/개발 대상**                |

> 빌드 오류의 대부분이 **루트 RN 흔적과 FE(0.73.9) 설정 혼합**에서 발생합니다.
> **항상 `FE` 디렉토리 안에서만** 모바일 빌드/실행을 수행하세요.

---

## 🔧 백엔드 (BE)

### 기술 스택

- Django 5.1 · Django REST Framework 3.16.1
- MySQL (mysqlclient 2.2.7)
- Celery 5.5.3 (비동기 작업)
- AWS S3 (boto3 1.40.63)
- Pillow 12.0.0

### 실행 방법

```bash
# 1) 진입
cd BE/

# 2) 가상환경 생성 및 활성화
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3) 의존성 설치
pip install -r requirements.txt

# 4) 환경변수(.env) 준비
#   - DATABASE_URL
#   - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
#   - SECRET_KEY

# 5) 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 6) 서버 실행
python manage.py runserver
# 서버: http://127.0.0.1:8000
```

---

## 📱 프론트엔드 (FE)

### 기술 스택

- React Native 0.73.9 · TypeScript 5.0.4
- React Navigation 6.x
- Axios 1.13.1
- AsyncStorage 1.24.0
- react-native-vector-icons 10.3.0

### 주요 화면

| 화면     | 파일                  | 내용               |
| -------- | --------------------- | ------------------ |
| 홈       | `HomeScreen.tsx`      | 메인 대시보드      |
| 탐지     | `DetectScreen.tsx`    | 미디어 진위 탐지   |
| 보호     | `ProtectScreen.tsx`   | 미디어 보호        |
| 워터마크 | `WatermarkScreen.tsx` | 워터마크 추가      |
| 히스토리 | `HistoryScreen.tsx`   | 작업 이력          |
| 뉴스     | `NewsScreen.tsx`      | 딥페이크 관련 뉴스 |

### 실행 방법

```bash
# 1) 진입
cd FE/

# 2) 의존성 설치
npm install

# 3) Metro 시작
npm start

# 4) Android 빌드/실행 (새 터미널)
npm run android

# 5) iOS (macOS 전용)
npm run ios
```

### API 통신 설정 예시

```ts
// FE/src/api/apiClient.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  timeout: 10_000,
});
```

---

## ⚠️ 현재 알려진 이슈 (Android/Gradle)

**현상 (FE/android):**

- `Plugin with id 'com.facebook.react' not found`
- `compileSdkVersion is not specified`

**해결 진행 상황:**

- @react-native/gradle-plugin 버전 **0.82.1 → 0.73.5**로 조정 ✅
- `npm install` 재실행으로 노드 모듈 설치 완료(984 패키지) ✅
- `node_modules/@react-native/gradle-plugin` 폴더 존재 확인 ✅
- `apply plugin: "com.facebook.react.rootproject"` 시도 → **해당 플러그인 미존재로 실패** ❌

**의심 원인:**

- `settings.gradle`의 플러그인 포함 경로 인식 불가(상대 경로 문제 가능)

**권장 조치 순서:**

1. **공식 템플릿과 파일 비교**

```bash
npx react-native@0.73.9 init TestProject
# 아래 파일 비교
# TestProject/android/build.gradle      ↔  FE/android/build.gradle
# TestProject/android/app/build.gradle  ↔  FE/android/app/build.gradle
# TestProject/android/settings.gradle   ↔  FE/android/settings.gradle
```

2. **Gradle 캐시/빌드 폴더 정리**

```bash
cd FE/android
rmdir /s /q .gradle
rmdir /s /q build
rmdir /s /q app\build
gradlew clean --refresh-dependencies
```

3. **settings.gradle 경로를 절대 경로로 명시**

```gradle
// FE/android/settings.gradle (예시)
def nodeModules = file("../../node_modules").absolutePath
includeBuild("$nodeModules/@react-native/gradle-plugin")

// RN 0.73 가이드에 맞춰 pluginManagement / dependencyResolutionManagement 블록도
// 템플릿과 동일하게 정렬할 것
```

4. **루트 RN 흔적 비활성화**

- 저장소 루트의 `android/`, `ios/`, `App.tsx`, `package.json`은 **빌드 대상 아님**
- CI나 로컬 스크립트에서 루트 경로로 빌드하지 않도록 주의

---

## 🧩 백엔드 앱(Modules)

| 앱           | 기능                     |
| ------------ | ------------------------ |
| `detection`  | 미디어 진위 탐지 API     |
| `protection` | 미디어 보호(워터마크 등) |
| `reports`    | 분석 리포트 생성/조회    |
| `users`      | 인증/권한/사용자 관리    |
| `zoom`       | Zoom 통합 기능           |

---

## 🛠 개발 환경 요구사항

**Backend**

- Python 3.8+
- MySQL 5.7+
- pip

**Frontend**

- Node.js 20+
- npm 또는 yarn
- JDK 17 (Android)
- Android Studio (Android SDK/NDK)
- Xcode (iOS, macOS 전용)

---

## 🔒 환경 변수 예시(.env)

```
# BE/.env
SECRET_KEY=...
DATABASE_URL=mysql://USER:PASS@HOST:3306/DBNAME
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
```

---

## 🧪 실행 순서 요약

1. **백엔드**

   - `cd BE && python -m venv venv && activate`
   - `pip install -r requirements.txt`
   - `.env` 설정 → `migrate` → `runserver`

2. **프론트엔드**

   - `cd FE && npm install`
   - `npm start` (Metro)
   - 별도 터미널에서 `npm run android` 또는 `npm run ios`

---

## 🗓 개발 히스토리 (요약)

- 2025-11-02

  - RN Gradle 플러그인 호환성 이슈 확인
  - `@react-native/gradle-plugin` 0.82.1 → 0.73.5 조정
  - `npm install` 재설치(984 패키지)
  - Android 빌드 에러 지속, 경로/템플릿 비교 예정

---

## 📌 운영 팁

- **항상 FE 폴더 기준**으로 RN 명령 수행
- Gradle 에러 시: **캐시 삭제 → 템플릿 비교 → 절대 경로 지정** 순으로 점검
- 루트 RN 유물은 건드리지 말고 **무시** (필요시 `/android`, `/ios`를 아카이빙)

---

## 📄 라이선스

프로젝트 라이선스를 `LICENSE` 파일로 추가하세요.

---

## 👥 기여자

팀 IM
(필요 시 개별 기여자/역할 표기)
