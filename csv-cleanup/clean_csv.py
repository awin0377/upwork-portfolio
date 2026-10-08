#!/usr/bin/env python3
"""CSV cleanup demo: messy product list -> clean, import-ready CSV + a short report.
Usage: python3 clean_csv.py messy_products.csv  (writes clean_products.csv, rejected_rows.csv, report.md)
Standard library only. Sample data is fictional."""
import csv, re, sys, collections
from datetime import datetime

CATEGORY_MAP = {'home office': 'Home Office', 'kitchen': 'Kitchen', 'audio': 'Audio', 'outdoor': 'Outdoor', 'outdoors': 'Outdoor'}
DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%b %d, %Y', '%Y.%m.%d']

def clean_name(s):
    out = []
    for w in s.strip().split():
        w = w.lower() if re.search(r'\d', w) else w.capitalize()
        out.append(re.sub(r'(\d)l$', r'\1L', w))
    return ' '.join(out)
def clean_category(s): return CATEGORY_MAP.get(s.strip().lower(), s.strip().title())
def clean_price(s):
    m = re.search(r'\d[\d,]*\.?\d*', s.replace(' ', ''))
    return f"{float(m.group().replace(',', '')):.2f}" if m else ''
def clean_stock(s):
    s = s.strip()
    return str(int(s)) if s.isdigit() else ''
def clean_date(s):
    s = s.strip()
    for f in DATE_FORMATS:
        try: return datetime.strptime(s, f).strftime('%Y-%m-%d')
        except ValueError: pass
    return ''
def clean_email(s):
    s = s.strip().lower()
    return s if re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-z]{2,}', s) else ''

def main(path):
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    out, rejected, seen = [], [], set()
    fixes = collections.Counter()
    for r in rows:
        sku = r['SKU'].strip().upper()
        if not sku:
            rejected.append({**r, 'Reason': 'missing SKU'}); continue
        if sku in seen:
            rejected.append({**r, 'Reason': 'duplicate SKU'}); continue
        seen.add(sku)
        c = {'SKU': sku, 'Product Name': clean_name(r['Product Name']), 'Category': clean_category(r['Category']),
             'Price': clean_price(r['Price']), 'Stock': clean_stock(r['Stock']), 'Updated': clean_date(r['Updated']),
             'Contact Email': clean_email(r['Contact Email'])}
        for k, v in c.items():
            if k != 'SKU' and v != r[k]: fixes[k] += 1
        for k in ('Price', 'Stock', 'Updated', 'Contact Email'):
            if not c[k]: fixes['needs review: ' + k] += 1
        out.append(c)
    with open('clean_products.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    with open('rejected_rows.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) + ['Reason']); w.writeheader(); w.writerows(rejected)
    lines = ['# CSV cleanup report', '', f'- Input rows: {len(rows)}', f'- Clean rows (import-ready): {len(out)}',
             f'- Rejected rows: {len(rejected)} (see rejected_rows.csv)', '', '## Fixes applied (count of cells changed)']
    lines += [f'- {k}: {v}' for k, v in sorted(fixes.items())]
    open('report.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'messy_products.csv')
