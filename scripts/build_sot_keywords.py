import csv, math
from collections import Counter

files = [
    'C:/Users/D E L L/Downloads/Keywords for SoT/Keyword Stats 2026-03-09 at 16_52_41.csv',
    'C:/Users/D E L L/Downloads/Keywords for SoT/Keyword Stats 2026-03-09 at 16_54_52.csv',
    'C:/Users/D E L L/Downloads/Keywords for SoT/Keyword Stats 2026-03-09 at 16_55_12.csv',
]

new_rows = []
for f in files:
    with open(f, encoding='utf-16') as fh:
        lines = fh.readlines()
    reader = csv.DictReader(lines[2:], delimiter='\t')
    for row in reader:
        kw = row.get('Keyword','').strip()
        sv_raw = row.get('Avg. monthly searches','').strip()
        comp = row.get('Competition','').strip()
        bid_high = row.get('Top of page bid (high range)','').strip()
        if not kw or not sv_raw:
            continue
        try:
            sv = int(sv_raw.replace(',',''))
            bh_usd = float(bid_high.replace(',','')) / 84 if bid_high else 0
        except:
            continue
        new_rows.append({'keyword': kw, 'sv': sv, 'competition': comp, 'cpc': bh_usd})

master_rows = []
with open('c:/Users/D E L L/Downloads/Claude Coded/SellonTube/research/keywords/master_keywords_cleaned.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            kw = row['keyword'].strip()
            sv = float(row['search_volume'] or 0)
            cpc = float(row['cpc'] or 0)
            kd = float(row['keyword_difficulty'] or 0)
            intent = row['search_intent'].strip().lower()
            cluster = row['topic_cluster']
        except:
            continue
        master_rows.append({'keyword': kw, 'sv': sv, 'cpc': cpc, 'kd': kd, 'intent': intent, 'cluster': cluster})

sot_include = [
    'youtube for business', 'youtube business', 'youtube marketing', 'youtube advertising',
    'youtube promotion', 'youtube channel promotion', 'youtube video promotion',
    'youtube for b2b', 'b2b youtube', 'youtube b2b',
    'youtube lead', 'lead gen youtube', 'youtube lead gen', 'youtube lead generation',
    'youtube customer', 'customer acquisition', 'youtube for lead',
    'video marketing', 'b2b video', 'video strategy', 'video content strategy',
    'video marketing strategy', 'video content marketing',
    'youtube content strategy', 'youtube marketing strategy', 'youtube channel strategy',
    'youtube growth strategy', 'youtube strategy',
    'video seo', 'youtube seo', 'youtube video seo',
    'youtube ads', 'youtube advertising cost', 'youtube ad campaign',
    'explainer video', 'video testimonial', 'product video', 'demo video',
    'brand video', 'corporate video', 'promotional video', 'customer testimonial',
    'youtube roi', 'video roi', 'youtube metrics', 'youtube analytics for',
    'video marketing roi', 'youtube channel analytics',
    'youtube organic', 'organic youtube',
    'youtube marketing agency', 'video marketing agency', 'youtube agency',
    'marketing agency youtube', 'video marketing service', 'youtube management',
    'youtube consulting', 'youtube consultant',
    'youtube sales', 'youtube funnel', 'video sales', 'video funnel',
    'brand youtube', 'youtube for brand',
    'youtube vs linkedin', 'youtube vs facebook', 'youtube vs instagram',
    'youtube vs tiktok', 'video vs blog', 'youtube vs podcast',
    'youtube for saas', 'saas youtube', 'youtube for startup',
    'youtube channel for business', 'business youtube channel',
    'animated explainer',
    'youtube businesses',
]

sot_exclude = [
    'free views', 'buy views', 'bot views',
    'youtube premium', 'youtube kids', 'youtube music', 'youtube tv',
    'screen record', 'loom', 'vidyard chrome',
    'video hosting', 'video player', 'video upload', 'free video hosting',
    'youtube download', 'download youtube',
    'adsense', ' rpm ', ' cpm ',
    'grow with jo', 'think and grow rich', 'grow young fitness',
    'free subscribers', 'youtube trending', 'trending youtube',
    'youtube tags', 'tag generator', 'thumbnail',
    'youtube shorts', 'instagram reels',
    'video editing', 'video editor', 'video maker', 'video cutter',
    'animation software', 'whiteboard animation',
    'screen recorder', 'chrome extension',
    'youtube reddit',
]

def is_sot(kw):
    kl = kw.lower()
    if any(e in kl for e in sot_exclude):
        return False
    return any(p in kl for p in sot_include)

filtered_new = [r for r in new_rows if is_sot(r['keyword']) and r['sv'] >= 50]
filtered_master = [r for r in master_rows if is_sot(r['keyword']) and r['sv'] >= 100]

merged = {}
for r in filtered_master:
    k = r['keyword'].lower().strip()
    merged[k] = {'keyword': r['keyword'], 'sv': r['sv'], 'cpc': r['cpc'],
                 'kd': r.get('kd', 0), 'intent': r.get('intent',''), 'cluster': r.get('cluster','')}

for r in filtered_new:
    k = r['keyword'].lower().strip()
    if k in merged:
        merged[k]['sv'] = max(merged[k]['sv'], r['sv'])
        if r['cpc'] > merged[k]['cpc']:
            merged[k]['cpc'] = r['cpc']
    else:
        merged[k] = {'keyword': r['keyword'], 'sv': r['sv'], 'cpc': r['cpc'], 'kd': 0, 'intent': '', 'cluster': ''}

rows = list(merged.values())

def categorize(kw):
    kl = kw.lower()
    if any(x in kl for x in ['seo agency', 'seo service', 'seo company', 'marketing agency', 'marketing service', 'marketing company', 'ads agency', 'advertising agency', 'advertising service', 'youtube management', 'youtube consulting', 'youtube consultant', 'video marketing agency', 'video marketing service']):
        return 'Agency / Services'
    if any(x in kl for x in ['explainer video', 'animated explainer', '2d explainer', '3d explainer', 'motion graphics', 'startup explainer', 'corporate explainer', 'product explainer']):
        return 'Explainer Video'
    if any(x in kl for x in ['video testimonial', 'customer testimonial', 'testimonial video']):
        return 'Video Testimonial'
    if any(x in kl for x in ['video seo', 'youtube seo', 'youtube video seo']):
        return 'YouTube SEO'
    if any(x in kl for x in ['youtube ads', 'youtube advertising', 'youtube ad campaign', 'youtube ad ', 'trueview']):
        return 'YouTube Advertising'
    if any(x in kl for x in ['video marketing strategy', 'video marketing', 'b2b video', 'video strategy', 'video content']):
        return 'Video Marketing Strategy'
    if any(x in kl for x in ['youtube marketing strategy', 'youtube content strategy', 'youtube channel strategy', 'youtube growth strategy', 'youtube strategy', 'youtube channel for business', 'business youtube channel', 'youtube for business', 'youtube business', 'youtube businesses', 'youtube marketing', 'youtube channel promotion']):
        return 'YouTube for Business'
    if any(x in kl for x in ['lead gen', 'youtube lead', 'customer acquisition', 'youtube funnel', 'youtube sales', 'youtube for lead']):
        return 'YouTube Lead Gen'
    if any(x in kl for x in ['youtube roi', 'video roi', 'youtube metrics', 'video marketing roi', 'youtube analytics']):
        return 'Analytics & ROI'
    if any(x in kl for x in ['youtube vs', 'video vs']):
        return 'Comparison'
    return 'Other'

for r in rows:
    r['category'] = categorize(r['keyword'])

rows = [r for r in rows if r['category'] != 'Other']

max_sv = max(r['sv'] for r in rows)
max_cpc = max(r['cpc'] for r in rows) or 1
for r in rows:
    kd_norm = 1 - min(r['kd'] / 100, 1)
    r['score'] = (r['sv']/max_sv)*0.45 + (r['cpc']/max_cpc)*0.35 + kd_norm*0.20

rows.sort(key=lambda x: -x['score'])

print(f"Total SoT keywords: {len(rows)}\n")
print(f"{'#':<3} {'Keyword':<56} {'SV':>8}  {'CPC':>8}  {'KD':>4}  Category")
print("-"*115)
for i, r in enumerate(rows[:60], 1):
    print(f"{i:<3} {r['keyword']:<56} {int(r['sv']):>8,}  ${r['cpc']:>7,.0f}  {int(r['kd']):>4}  {r['category']}")

print("\nCategory breakdown (all):")
cat_counts = Counter(r['category'] for r in rows)
for cat, cnt in cat_counts.most_common():
    print(f"  {cat}: {cnt}")

# Save CSV
out_path = 'c:/Users/D E L L/Downloads/Claude Coded/SellonTube/research/keywords/sot_keywords.csv'
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['rank','keyword','search_volume','cpc_usd','keyword_difficulty','intent','category','cluster'])
    writer.writeheader()
    for i, r in enumerate(rows, 1):
        writer.writerow({
            'rank': i,
            'keyword': r['keyword'],
            'search_volume': int(r['sv']),
            'cpc_usd': round(r['cpc'], 2),
            'keyword_difficulty': int(r['kd']),
            'intent': r['intent'],
            'category': r['category'],
            'cluster': r['cluster'],
        })
print(f"\nSaved: {out_path} ({len(rows)} rows)")
