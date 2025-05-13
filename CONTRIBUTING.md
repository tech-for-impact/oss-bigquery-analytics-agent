# 🛠️ 프로젝트 기여 가이드

이 문서는 오픈소스 프로젝트에 기여하고자 하는 개발자분들을 위한 가이드입니다. 기여 전 꼭 한 번 읽어봐 주세요.

---

## 1. 서론

프로젝트에 관심을 가져주셔서 감사합니다! 본 가이드는 이슈 제보, 기능 제안, 버그 수정, 문서 개선 등의 기여 과정을 단계별로 안내합니다.

## 2. 기여 원칙

* **존중과 예의**: 모든 참여자는 서로를 존중하며 건설적인 피드백을 제공합니다.
* **일관성**: 기존 코드 스타일과 컴포넌트 구조를 따릅니다.
* **투명성**: 변경 사항은 명확한 커밋 메시지와 PR 설명으로 기록합니다.

## 3. 이슈 보고 (Issue)

1. 저장소의 **Issues** 탭으로 이동합니다.
2. 새 이슈를 열기 전에 기존 이슈와 중복되는지 검색합니다.
3. 제목(Title)과 본문(Description)에 다음 정보를 포함합니다:

   * 문제의 요약
   * 재현 방법(steps to reproduce)
   * 기대 결과와 실제 결과
   * 환경 정보(OS, Node.js/Python 버전 등)

## 4. 개발 환경 설정

1. 저장소를 포크(fork)하고 로컬에 클론(clone)합니다:

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. 원본 저장소를 `upstream` 리모트로 추가합니다:

   ```bash
   git remote add upstream https://github.com/<original-owner>/<repo-name>.git
   ```
3. 필요한 의존성을 설치합니다:

   ```bash
   pip install -e .
   ```
4. 개발용 브랜치를 생성하고 전환합니다:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## 5. 코드 스타일
추후 작성 예쩡

## 6. Pull Request 제출

1. 로컬 브랜치에서 작업을 완료한 후 커밋합니다:

   ```bash
   git add .
   git commit -m "feat: 짧은 설명 (#이슈번호)"
   ```
2. 원격 저장소에 푸시합니다:

   ```bash
   git push origin feature/your-feature-name
   ```
3. GitHub에서 **Pull Request**를 생성하고 다음을 기재합니다:

   * 어떤 변경을 했는지 요약
   * 왜 필요한 변경인지 설명
   * 관련 이슈 번호

## 7. 코드 리뷰 및 병합

* 프로젝트 유지 관리자는 PR을 리뷰하고 피드백을 제공합니다.
* 리뷰 요청에 따라 코드 수정 후 푸시하면, PR에 자동으로 반영됩니다.
* 모든 리뷰가 통과되면 PR이 병합됩니다.

## 8. 커뮤니케이션
- 업데이터 예정

## 9. 감사의 말

여러분의 기여 덕분에 프로젝트가 더욱 발전합니다. 언제나 열린 마음으로 환영합니다!

---

*이 가이드는 필요에 따라 업데이트될 수 있습니다.*
