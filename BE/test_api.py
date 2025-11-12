"""
딥페이크 감지 앱 - 완벽한 API 통합 테스트 스크립트
실행: python test_api.py
"""

import requests
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

# ============================================
# 설정
# ============================================
BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com"
TEST_PASSWORD = "testpass123!"
TEST_NICKNAME = "테스트유저"

# 테스트용 더미 파일 생성 (Windows/Mac/Linux 모두 호환)
TEMP_DIR = tempfile.gettempdir()
TEST_IMAGE_PATH = os.path.join(TEMP_DIR, "test_image.jpg")
TEST_VIDEO_PATH = os.path.join(TEMP_DIR, "test_video.mp4")

# 전역 변수
token = None
user_id = None
record_id = None
job_id = None
session_id = None
report_id = None


# ============================================
# 유틸리티 함수
# ============================================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_test_header(test_name):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}테스트: {test_name}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")


def print_success(message):
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")


def print_error(message):
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")


def print_info(message):
    print(f"{Colors.OKCYAN}ℹ️  {message}{Colors.ENDC}")


def print_response(response):
    print(f"{Colors.OKBLUE}응답 코드: {response.status_code}{Colors.ENDC}")
    try:
        data = response.json()
        print(f"{Colors.OKBLUE}응답 데이터: {json.dumps(data, indent=2, ensure_ascii=False)}{Colors.ENDC}")
    except:
        print(f"{Colors.OKBLUE}응답 데이터: {response.text[:500]}{Colors.ENDC}")
    
    # 에러 상세 정보
    if response.status_code >= 400:
        print(f"{Colors.FAIL}❌ HTTP {response.status_code} 에러 발생!{Colors.ENDC}")
        try:
            error_data = response.json()
            if 'detail' in error_data:
                print(f"{Colors.FAIL}상세: {error_data['detail']}{Colors.ENDC}")
            if 'error' in error_data:
                print(f"{Colors.FAIL}에러: {error_data['error']}{Colors.ENDC}")
        except:
            pass


def create_dummy_image():
    """테스트용 더미 이미지 생성"""
    try:
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(TEST_IMAGE_PATH)
        print_success(f"더미 이미지 생성: {TEST_IMAGE_PATH}")
    except ImportError:
        # PIL 없으면 빈 파일 생성
        with open(TEST_IMAGE_PATH, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')  # PNG 헤더
        print_success(f"더미 이미지 생성: {TEST_IMAGE_PATH} (빈 파일)")


def create_dummy_video():
    """테스트용 더미 비디오 생성"""
    with open(TEST_VIDEO_PATH, 'wb') as f:
        f.write(b'\x00\x00\x00\x18ftypmp42')  # MP4 헤더
    print_success(f"더미 비디오 생성: {TEST_VIDEO_PATH}")


# ============================================
# 1. Users 앱 테스트
# ============================================
def test_user_register():
    """회원가입 테스트"""
    print_test_header("1-1. 회원가입")
    
    url = f"{BASE_URL}/api/users/register/"
    data = {
        "email": TEST_EMAIL,
        "nickname": TEST_NICKNAME,
        "password": TEST_PASSWORD,
        "password_confirm": TEST_PASSWORD
    }
    
    print_info(f"POST {url}")
    print_info(f"데이터: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(url, json=data)
    print_response(response)
    
    if response.status_code == 201:
        global token, user_id
        result = response.json()
        token = result.get('token')
        user_id = result.get('user', {}).get('user_id')
        print_success(f"회원가입 성공! Token: {token[:20]}... User ID: {user_id}")
        return True
    else:
        print_error("회원가입 실패!")
        return False


def test_user_login():
    """로그인 테스트"""
    print_test_header("1-2. 로그인")
    
    url = f"{BASE_URL}/api/users/login/"
    data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print_info(f"POST {url}")
    response = requests.post(url, json=data)
    print_response(response)
    
    if response.status_code == 200:
        global token
        result = response.json()
        token = result.get('token')
        print_success(f"로그인 성공! Token: {token[:20]}...")
        return True
    else:
        print_error("로그인 실패!")
        return False


def test_user_profile():
    """프로필 조회 테스트"""
    print_test_header("1-3. 프로필 조회")
    
    url = f"{BASE_URL}/api/users/profile/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    print_info(f"Header: Authorization: Token {token[:20]}...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("프로필 조회 성공!")
        return True
    else:
        print_error("프로필 조회 실패!")
        return False


# ============================================
# 2. Detection 앱 테스트
# ============================================
def test_analyze_image():
    """이미지 분석 테스트"""
    print_test_header("2-1. 이미지 분석")
    
    url = f"{BASE_URL}/api/detection/image/"
    headers = {"Authorization": f"Token {token}"}
    
    create_dummy_image()
    
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'image': ('test.jpg', f, 'image/jpeg')}  # file → image
        
        print_info(f"POST {url}")
        response = requests.post(url, headers=headers, files=files)
    
    print_response(response)
    
    if response.status_code in [200, 201]:
        global record_id
        result = response.json()
        record_id = result.get('record_id')
        print_success(f"이미지 분석 요청 성공! Record ID: {record_id}")
        return True
    else:
        print_error("이미지 분석 실패!")
        return False


def test_analyze_video():
    """영상 분석 테스트"""
    print_test_header("2-2. 영상 분석")
    
    url = f"{BASE_URL}/api/detection/video/"
    headers = {"Authorization": f"Token {token}"}
    
    create_dummy_video()
    
    with open(TEST_VIDEO_PATH, 'rb') as f:
        files = {'video': ('test.mp4', f, 'video/mp4')}  # file → video
        
        print_info(f"POST {url}")
        response = requests.post(url, headers=headers, files=files)
    
    print_response(response)
    
    if response.status_code in [200, 201]:
        print_success("영상 분석 요청 성공!")
        return True
    else:
        print_error("영상 분석 실패!")
        return False


def test_get_records():
    """분석 기록 목록 조회 테스트"""
    print_test_header("2-3. 분석 기록 목록 조회")
    
    url = f"{BASE_URL}/api/detection/records/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("분석 기록 조회 성공!")
        return True
    else:
        print_error("분석 기록 조회 실패!")
        return False


def test_get_record_detail():
    """분석 기록 상세 조회 테스트"""
    print_test_header("2-4. 분석 기록 상세 조회")
    
    if not record_id:
        print_error("Record ID가 없습니다. 이미지 분석을 먼저 실행하세요.")
        return False
    
    url = f"{BASE_URL}/api/detection/records/{record_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("분석 기록 상세 조회 성공!")
        return True
    else:
        print_error("분석 기록 상세 조회 실패!")
        return False


def test_get_statistics():
    """통계 조회 테스트"""
    print_test_header("2-5. 통계 조회")
    
    url = f"{BASE_URL}/api/detection/statistics/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("통계 조회 성공!")
        return True
    else:
        print_error("통계 조회 실패!")
        return False


# ============================================
# 3. Protection 앱 테스트
# ============================================
def test_protect_image():
    """이미지 보호 테스트"""
    print_test_header("3-1. 이미지 보호")
    
    url = f"{BASE_URL}/api/protection/images/"
    headers = {"Authorization": f"Token {token}"}
    
    create_dummy_image()
    
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'files': ('test.jpg', f, 'image/jpeg')}  # image → files (복수)
        
        print_info(f"POST {url}")
        response = requests.post(url, headers=headers, files=files)
    
    print_response(response)
    
    if response.status_code in [200, 201]:
        global job_id
        result = response.json()
        job_id = result.get('job_id')
        print_success(f"이미지 보호 요청 성공! Job ID: {job_id}")
        return True
    else:
        print_error("이미지 보호 실패!")
        return False


def test_protect_video():
    """영상 보호 테스트"""
    print_test_header("3-2. 영상 보호")
    
    url = f"{BASE_URL}/api/protection/videos/"
    headers = {"Authorization": f"Token {token}"}
    
    create_dummy_video()
    
    with open(TEST_VIDEO_PATH, 'rb') as f:
        files = {'file': ('test.mp4', f, 'video/mp4')}
        
        print_info(f"POST {url}")
        response = requests.post(url, headers=headers, files=files)
    
    print_response(response)
    
    if response.status_code in [200, 201]:
        print_success("영상 보호 요청 성공!")
        return True
    else:
        print_error("영상 보호 실패!")
        return False


def test_get_jobs():
    """작업 목록 조회 테스트"""
    print_test_header("3-3. 작업 목록 조회")
    
    url = f"{BASE_URL}/api/protection/jobs/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("작업 목록 조회 성공!")
        return True
    else:
        print_error("작업 목록 조회 실패!")
        return False


def test_get_job_detail():
    """작업 상태 조회 테스트"""
    print_test_header("3-4. 작업 상태 조회")
    
    if not job_id:
        print_error("Job ID가 없습니다. 이미지 보호를 먼저 실행하세요.")
        return False
    
    url = f"{BASE_URL}/api/protection/jobs/{job_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("작업 상태 조회 성공!")
        return True
    else:
        print_error("작업 상태 조회 실패!")
        return False


# ============================================
# 4. Zoom 앱 테스트
# ============================================
def test_start_zoom_session():
    """줌 세션 시작 테스트"""
    print_test_header("4-1. 줌 세션 시작")
    
    url = f"{BASE_URL}/api/zoom/sessions/start/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "session_name": "테스트 면접"
    }
    
    print_info(f"POST {url}")
    response = requests.post(url, headers=headers, json=data)
    print_response(response)
    
    if response.status_code in [200, 201]:
        global session_id
        result = response.json()
        session_id = result.get('session_id')
        print_success(f"줌 세션 시작 성공! Session ID: {session_id}")
        return True
    else:
        print_error("줌 세션 시작 실패!")
        return False


def test_capture_zoom():
    """줌 캡처 분석 테스트"""
    print_test_header("4-2. 줌 캡처 분석")
    
    if not session_id:
        print_error("Session ID가 없습니다. 줌 세션을 먼저 시작하세요.")
        return False
    
    url = f"{BASE_URL}/api/zoom/sessions/{session_id}/capture/"
    headers = {"Authorization": f"Token {token}"}
    
    create_dummy_image()
    
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'screenshot': ('capture.jpg', f, 'image/jpeg')}
        data = {'participant_count': 2}  # 참가자 수 추가
        
        print_info(f"POST {url}")
        response = requests.post(url, headers=headers, files=files, data=data)
    
    print_response(response)
    
    if response.status_code in [200, 201]:
        print_success("줌 캡처 분석 성공!")
        return True
    else:
        print_error("줌 캡처 분석 실패!")
        return False


def test_end_zoom_session():
    """줌 세션 종료 테스트"""
    print_test_header("4-3. 줌 세션 종료")
    
    if not session_id:
        print_error("Session ID가 없습니다. 줌 세션을 먼저 시작하세요.")
        return False
    
    url = f"{BASE_URL}/api/zoom/sessions/{session_id}/end/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"POST {url}")
    response = requests.post(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("줌 세션 종료 성공!")
        return True
    else:
        print_error("줌 세션 종료 실패!")
        return False


def test_get_zoom_report():
    """줌 보고서 조회 테스트"""
    print_test_header("4-4. 줌 보고서 조회")
    
    if not session_id:
        print_error("Session ID가 없습니다. 줌 세션을 먼저 시작하세요.")
        return False
    
    url = f"{BASE_URL}/api/zoom/sessions/{session_id}/report/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("줌 보고서 조회 성공!")
        return True
    else:
        print_error("줌 보고서 조회 실패!")
        return False


# ============================================
# 5. Reports 앱 테스트
# ============================================
def test_submit_report():
    """신고 접수 테스트"""
    print_test_header("5-1. 신고 접수")
    
    if not record_id:
        print_error("Record ID가 없습니다. 이미지 분석을 먼저 실행하세요.")
        return False
    
    url = f"{BASE_URL}/api/reports/submit/"
    headers = {"Authorization": f"Token {token}"}
    
    data = {
        "record_id": record_id,
        "report_type": "deepfake_image",
        "discovery_source": "sns",
        "damage_level": "personal",  # ← 올바른 값!
        "description": "테스트 신고입니다.",
        "report_agency": "kisa"
    }
    
    print_info(f"POST {url}")
    print_info(f"데이터: {json.dumps(data, ensure_ascii=False)}")
    response = requests.post(url, headers=headers, json=data)
    print_response(response)
    
    if response.status_code in [200, 201]:
        global report_id
        result = response.json()
        report_id = result.get('report_id')
        print_success(f"신고 접수 성공! Report ID: {report_id}")
        return True
    else:
        print_error("신고 접수 실패!")
        return False


def test_get_my_reports():
    """내 신고 내역 조회 테스트"""
    print_test_header("5-2. 내 신고 내역 조회")
    
    url = f"{BASE_URL}/api/reports/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("내 신고 내역 조회 성공!")
        return True
    else:
        print_error("내 신고 내역 조회 실패!")
        return False


def test_get_report_detail():
    """신고 상세 조회 테스트"""
    print_test_header("5-3. 신고 상세 조회")
    
    if not report_id:
        print_error("Report ID가 없습니다. 신고를 먼저 접수하세요.")
        return False
    
    url = f"{BASE_URL}/api/reports/{report_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    print_info(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print_success("신고 상세 조회 성공!")
        return True
    else:
        print_error("신고 상세 조회 실패!")
        return False


# ============================================
# 메인 실행
# ============================================
def main():
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║           딥페이크 감지 앱 - API 통합 테스트              ║
║                    완벽한 테스트 스크립트                 ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"테스트 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 1. Users 앱 테스트
    results.append(("회원가입", test_user_register()))
    results.append(("로그인", test_user_login()))
    results.append(("프로필 조회", test_user_profile()))
    
    # 2. Detection 앱 테스트
    results.append(("이미지 분석", test_analyze_image()))
    results.append(("영상 분석", test_analyze_video()))
    results.append(("분석 기록 목록", test_get_records()))
    results.append(("분석 기록 상세", test_get_record_detail()))
    results.append(("통계 조회", test_get_statistics()))
    
    # 3. Protection 앱 테스트
    results.append(("이미지 보호", test_protect_image()))
    results.append(("영상 보호", test_protect_video()))
    results.append(("작업 목록 조회", test_get_jobs()))
    results.append(("작업 상태 조회", test_get_job_detail()))
    
    # 4. Zoom 앱 테스트
    results.append(("줌 세션 시작", test_start_zoom_session()))
    results.append(("줌 캡처 분석", test_capture_zoom()))
    results.append(("줌 세션 종료", test_end_zoom_session()))
    results.append(("줌 보고서 조회", test_get_zoom_report()))
    
    # 5. Reports 앱 테스트
    results.append(("신고 접수", test_submit_report()))
    results.append(("내 신고 내역", test_get_my_reports()))
    results.append(("신고 상세 조회", test_get_report_detail()))
    
    # 결과 요약
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}테스트 결과 요약{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for name, result in results:
        status = f"{Colors.OKGREEN}✅ PASS{Colors.ENDC}" if result else f"{Colors.FAIL}❌ FAIL{Colors.ENDC}"
        print(f"{status} - {name}")
    
    print(f"\n{Colors.BOLD}총 {len(results)}개 테스트 중:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✅ 성공: {passed}개{Colors.ENDC}")
    print(f"{Colors.FAIL}❌ 실패: {failed}개{Colors.ENDC}")
    print(f"{Colors.BOLD}성공률: {(passed/len(results)*100):.1f}%{Colors.ENDC}\n")
    
    # 정리
    for path in [TEST_IMAGE_PATH, TEST_VIDEO_PATH]:
        if os.path.exists(path):
            os.remove(path)
            print_info(f"임시 파일 삭제: {path}")
    
    print_info(f"테스트 종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}테스트가 사용자에 의해 중단되었습니다.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}예상치 못한 오류 발생: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()