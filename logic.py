from playwright.sync_api import sync_playwright, TimeoutError

def parse_case_row(row_locator,page):
    serial = row_locator.locator('td.sorting_1').text_content().strip()
    second_td = row_locator.locator('td').nth(1)
    case_type = second_td.locator('a').first.text_content().strip()
    second_td_text = second_td.inner_text()
    split_text = second_td_text.split(case_type + " - ")
    case_number = ""
    if len(split_text) > 1:
        case_number = split_text[1].split('\n')[0]
    status = second_td.locator('font').text_content().strip()
    statusColor = second_td.locator('font').get_attribute('color')
    orders_url = second_td.locator('a:has-text("Orders")').get_attribute('href')
    third_td = row_locator.locator('td').nth(2)
    parties_lines = third_td.inner_text().split('\n')
    petitioner = parties_lines[0]
    respondent = parties_lines[2]
    fourth_td = row_locator.locator('td').nth(3)
    fourth_text = fourth_td.inner_text()
    next_date = ""
    last_date = ""
    court_no = ""
    for line in fourth_text.split('\n'):
        line = line.strip()
        if line.upper().startswith("NEXT DATE:"):
            next_date = line.split(":",1)[1].strip()
        elif line.upper().startswith("LAST DATE:"):
            last_date = line.split(":",1)[1].strip()
        elif line.upper().startswith("COURT NO:"):
            court_no = line.split(":",1)[1].strip()

    page.goto(orders_url)
    page.wait_for_function("""() => {const row = document.querySelector('#caseTable tbody tr td');
        if (!row) return false;
        return row.innerText.trim() !== 'Loading...';}""",timeout=1000)
    hrefs = page.locator('#caseTable tbody tr td a').evaluate_all('elements => elements.map(el => el.getAttribute("href"))')
    
    return {
        "serial": serial,
        "case_type": case_type,
        "case_number": case_number,
        "status": status,
        "statusColor": statusColor,
        "orders_url": orders_url,
        "orders_links": hrefs,
        "petitioner": petitioner,
        "respondent": respondent,
        "next_date": next_date,
        "last_date": last_date,
        "court_no": court_no
    }


def get_case_details(case_type: str, case_number: str, year: str) -> dict:
    context = None
    try:
        browser = sync_playwright().start().chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        page = context.new_page()
        page.route("**/*.{png,jpg,jpeg,css,woff2}", lambda route: route.abort())
        page.goto("https://delhihighcourt.nic.in/app/get-case-type-status")
        captcha_code = page.locator('#captcha-code').text_content() # type: ignore
        page.locator('input[name="captchaInput"]').fill(captcha_code) # type: ignore

        page.locator('select[name="case_type"]').select_option(case_type)
        page.locator('input[placeholder="Case Number :"]').fill(case_number)
        page.locator('select[name="case_year"]').select_option(year)
        page.get_by_role('button', name='Submit').click()

        page.wait_for_function("""() => {const row = document.querySelector('#caseTable tbody tr');
        if (!row) return false;
        return row.innerText.trim() !== 'No data available in table';}""",timeout=1000)
        op_json = parse_case_row(page.locator('#caseTable tbody tr').first,page)
        return op_json
    
    except TimeoutError:
        return None # type: ignore
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None # type: ignore
    finally:
        if context:

            context.close()
