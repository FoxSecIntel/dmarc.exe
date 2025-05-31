import gzip
import xml.etree.ElementTree as ET

def parse_dmarc_gzip(file_path):
    try:
        with gzip.open(file_path, 'rb') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            results = []
            for rec in root.findall('record'):
                results.append({
                    'source_ip': rec.findtext('row/source_ip'),
                    'count': rec.findtext('row/count'),
                    'disposition': rec.findtext('row/policy_evaluated/disposition'),
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]
