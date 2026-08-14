"""
クラブ飛距離メモアプリ E2Eテスト
Selenium + Python
事前準備: pip install selenium
実行方法: python test_club_distance.py
対象URL: http://localhost:5173（npm run devで起動しておくこと）
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# ========================================
# セットアップ
# ========================================
driver = webdriver.Chrome()
driver.get("http://localhost:5173")

# テスト前に既存の履歴を全削除（過去の実行で溜まったデータをクリア）
driver.execute_async_script("""
    const callback = arguments[arguments.length - 1];
    fetch('http://localhost:3001/api/history')
        .then(res => res.json())
        .then(records => Promise.all(
            records.map(r => fetch(`http://localhost:3001/api/history/${r.id}`, { method: 'DELETE' }))
        ))
        .then(() => callback())
        .catch(() => callback());
""")
driver.refresh()

wait = WebDriverWait(driver, 10)

# クラブ一覧のAPI取得が完了する（ドロップダウンに選択肢が入る）まで待つ
wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "option")) > 0)


def set_input_value(element, value):
    """Reactのcontrolled inputに対して確実に値をセットする"""
    driver.execute_script(
        "const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;"
        "setter.call(arguments[0], arguments[1]);"
        "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
        element, value
    )


# ========================================
# テスト①：ページが正しく表示されるか
# ========================================
print("テスト① ページ表示...")

title = driver.find_element(By.TAG_NAME, "h1")
assert title.text == "クラブ飛距離メモ", f"タイトルが違う: {title.text}"

select = driver.find_element(By.TAG_NAME, "select")
assert select is not None

input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
assert input_field is not None

button = driver.find_element(By.TAG_NAME, "button")
assert button.text == "保存"

print("  → OK：ページ要素がすべて表示されている")


# ========================================
# テスト②：バリデーション（空欄）
# ========================================
print("テスト② バリデーション（空欄）...")

button = driver.find_element(By.TAG_NAME, "button")
button.click()

alert = wait.until(EC.alert_is_present())
assert "数値を入力してください" in alert.text
alert.accept()

print("  → OK：空欄でアラートが出た")


# ========================================
# テスト③：バリデーション（0以下）
# ========================================
print("テスト③ バリデーション（0以下）...")

input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
set_input_value(input_field, "-10")

button = driver.find_element(By.TAG_NAME, "button")
button.click()

alert = wait.until(EC.alert_is_present())
assert "ミスショット" in alert.text
alert.accept()

print("  → OK：0以下でアラートが出た")


# ========================================
# テスト④：正常な記録
# ========================================
print("テスト④ 正常な記録...")

input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
set_input_value(input_field, "160")

button = driver.find_element(By.TAG_NAME, "button")
button.click()

time.sleep(0.5)
input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
assert input_field.get_attribute("value") == "", "入力欄がリセットされていない"

history_toggle = driver.find_element(By.CLASS_NAME, "history-toggle")
history_toggle.click()

distances = driver.find_elements(By.CLASS_NAME, "stroke-distance")
distance_texts = [d.text for d in distances]
assert any("160" in t for t in distance_texts), "飛距離160が画面に表示されていない"

history_toggle.click()

print("  → OK：記録が保存され入力欄がリセットされた")


# ========================================
# テスト⑤：平均表示
# ========================================
print("テスト⑤ 平均表示...")

input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
set_input_value(input_field, "155")
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(0.3)

input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
set_input_value(input_field, "165")
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(0.3)

page_text = driver.find_element(By.CLASS_NAME, "result-card").text
assert "160" in page_text, f"平均160が表示されていない: {page_text}"

print("  → OK：直近3球の平均が正しく表示された")


# ========================================
# テスト⑥：クラブ切り替え
# ========================================
print("テスト⑥ クラブ切り替え...")

select_element = driver.find_element(By.TAG_NAME, "select")
select = Select(select_element)
select.select_by_value("8I")
time.sleep(0.3)

input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")
set_input_value(input_field, "148")
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(0.3)

page_text = driver.find_element(By.CLASS_NAME, "result-card").text
assert "148" in page_text, f"8Iの平均148が表示されていない: {page_text}"

print("  → OK：クラブ切り替えと記録が正常")


# ========================================
# テスト⑦：履歴の開閉
# ========================================
print("テスト⑦ 履歴の開閉...")

select_element = driver.find_element(By.TAG_NAME, "select")
select = Select(select_element)
select.select_by_value("1W")
time.sleep(0.3)

toggle_button = driver.find_element(By.CLASS_NAME, "history-toggle")
assert "履歴を見る" in toggle_button.text
toggle_button.click()
time.sleep(0.3)

history_rows = driver.find_elements(By.CLASS_NAME, "history-row")
assert len(history_rows) == 3, f"履歴が3件ではない: {len(history_rows)}件"

toggle_button = driver.find_element(By.CLASS_NAME, "history-toggle")
assert "閉じる" in toggle_button.text

print("  → OK：履歴の開閉が正常")


# ========================================
# テスト⑧：1件削除
# ========================================
print("テスト⑧ 1件削除...")

delete_buttons = driver.find_elements(By.CLASS_NAME, "delete-btn")
delete_buttons[0].click()
time.sleep(0.3)

history_rows = driver.find_elements(By.CLASS_NAME, "history-row")
assert len(history_rows) == 2, f"履歴が2件ではない: {len(history_rows)}件"

print("  → OK：1件削除が正常")


# ========================================
# テスト⑨：まとめて削除
# ========================================
print("テスト⑨ まとめて削除...")

delete_all_button = driver.find_element(By.CLASS_NAME, "delete-all-btn")
delete_all_button.click()
time.sleep(0.3)

history_rows = driver.find_elements(By.CLASS_NAME, "history-row")
assert len(history_rows) == 0, f"履歴が残っている: {len(history_rows)}件"

print("  → OK：まとめて削除が正常")


# ========================================
# テスト⑩：リロード後のデータ永続化
# ========================================
print("テスト⑩ リロード後の永続化...")

select_element = driver.find_element(By.TAG_NAME, "select")
select = Select(select_element)
select.select_by_value("8I")
time.sleep(0.3)

driver.refresh()
time.sleep(0.5)

select_element = driver.find_element(By.TAG_NAME, "select")
select = Select(select_element)
select.select_by_value("8I")
time.sleep(0.3)

page_text = driver.find_element(By.CLASS_NAME, "result-card").text
assert "148" in page_text, "リロード後にデータが消えた"

print("  → OK：リロード後もデータが残っている")


# ========================================
# 終了
# ========================================
print("")
print("=" * 40)
print("全テスト合格！")
print("=" * 40)

driver.quit()
