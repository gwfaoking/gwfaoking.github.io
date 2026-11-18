# gwfaoking.github.io

gwfaoking이 만든 모든 앱의 개인정보처리방침·약관을 공개하는 저장소입니다.
GitHub Pages로 공개되며, Play Console의 "개인정보처리방침 URL"에 이 주소를 넣습니다.

- 전체 목록: https://gwfaoking.github.io/
- 앱별 주소: `https://gwfaoking.github.io/<앱 id>/privacy/` (영문: `.../privacy/en.html`)

| 앱 | id | 개인정보처리방침 |
| --- | --- | --- |
| MOA 올인원 (`com.moa.allinone`) | `moa` | https://gwfaoking.github.io/moa/privacy/ |

## 구조

```
apps.json                  앱 목록 (id, 이름, 패키지명, 문서 종류)
src/<id>/PRIVACY.md        원본 (한국어)      ← 여기만 고칩니다
src/<id>/PRIVACY_en.md     원본 (영어, 선택)
src/<id>/TERMS.md          약관 (선택)
<id>/privacy/index.html    생성된 페이지 (직접 고치지 않음)
<id>/privacy/en.html
index.html                 생성된 전체 목록
tools/build.py             Markdown → HTML 생성기 (외부 패키지 없음)
```

## 앱 추가·수정 방법

1. `apps.json`에 앱을 추가합니다. `id`는 URL에 쓰이므로 한 번 정하면 바꾸지 않습니다.
   `documents`에는 `PRIVACY`, `TERMS` 중 있는 것만 적습니다.
2. `src/<id>/PRIVACY.md`(필요하면 `PRIVACY_en.md`, `TERMS.md`)를 넣습니다.
   앱 안에도 같은 방침을 보여 준다면, 앱 저장소의 원본을 그대로 복사해 두 곳이 같게 유지합니다.
3. `python3 tools/build.py`로 HTML을 만들고, 원본과 생성된 HTML을 같은 커밋으로 올립니다.
   CI(`check`)가 생성 결과가 원본과 다르면 실패합니다.

지원하는 Markdown: `#` 제목, 문단, `-`/`1.` 목록, `**굵게**`, `` `코드` ``, `[링크](https://...)`, 맨 URL.
