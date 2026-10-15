from flask import Flask, jsonify, request

app = Flask(__name__)


def insertion_sort_steps(arr):
  """단순 삽입 정렬(Insertion Sort) 알고리즘을 수행하며

  각 단계별 배열의 상태와 설명을 기록하여 반환합니다.
  """
  steps = []
  n = len(arr)

  # 1. 초기 상태 기록
  steps.append({
      'array': list(arr),
      'current': -1,
      'target': -1,
      'description': '초기 배열 상태입니다.',
  })

  # 두 번째 원소부터 마지막 원소까지 순회
  for i in range(1, n):
    key = arr[i]
    j = i - 1

    steps.append({
        'array': list(arr),
        'current': i,
        'target': j,
        'description': (
            f'원소 [{key}] (인덱스 {i})를 선택하여 정렬된 앞부분과 비교를 시작합니다.'
        ),
    })

    # 현재 key보다 큰 원소들을 오른쪽으로 한 칸씩 이동
    while j >= 0 and arr[j] > key:
      arr[j + 1] = arr[j]
      j -= 1
      steps.append({
          'array': list(arr),
          'current': j + 1,
          'target': j,
          'description': (
              f'원소가 더 큽니다. 오른쪽으로 이동 후 계속 비교합니다. (현재'
              f' 빈 자리 인덱스: {j+1})'
          ),
      })

    # 올바른 위치에 key 삽입
    arr[j + 1] = key
    steps.append({
        'array': list(arr),
        'current': j + 1,
        'target': -1,
        'description': (
            f'원소 [{key}]를 올바른 위치(인덱스 {j+1})에 삽입했습니다.'
        ),
    })

  # 최종 완료 상태 기록
  steps.append({
      'array': list(arr),
      'current': -1,
      'target': -1,
      'description': '단순 삽입 정렬이 성공적으로 완료되었습니다!',
  })

  return steps


@app.route('/sort', methods=['POST'])
def sort_array():
  """클라이언트로부터 POST 요청을 받아 정렬을 수행하고 결과를 반환하는 엔드포인트"""
  try:
    data = request.get_json()
    # 입력받은 배열 (기본값 제공)
    input_array = data.get('array', [8, 3, 5, 1, 4, 2])
    # 정수형으로 변환
    input_array = [int(x) for x in input_array]

    # 정렬 단계별 데이터 생성
    steps = insertion_sort_steps(input_array)

    # 단순 삽입 정렬 복잡도 정보 정의
    complexity_info = {
        'time_best': 'O(n) - 이미 정렬되어 있는 경우',
        'time_avg': 'O(n^2) - 평균적인 경우',
        'time_worst': 'O(n^2) - 역순으로 정렬된 경우',
        'space': 'O(1) - 제자리 정렬(In-place sorting)로 추가 공간 불필요',
    }

    return jsonify(
        {'status': 'success', 'steps': steps, 'complexity': complexity_info}
    )

  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 400


if __name__ == '__main__':
  # Cloud Run 환경 변수 포트 반영 (기본 8080)
  app.run(host='0.0.0.0', port=8080)
