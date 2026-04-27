import os
import csv
import ezdxf
from mcp.server.fastmcp import FastMCP

# Initialize MCP for CAD
mcp = FastMCP("Takon CAD")

@mcp.tool()
def extract_dxf_data(dxf_path: str) -> str:
    """Extract text and block data from a DXF file."""
    if not os.path.exists(dxf_path): return f"Error: File {dxf_path} not found."
    try:
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        results = []
        for e in msp.query('TEXT MTEXT'):
            results.append({"type": e.dxftype(), "content": e.dxf.text if e.dxftype() == 'TEXT' else e.text, "layer": e.dxf.layer})
        for e in msp.query('INSERT'):
            results.append({"type": "BLOCK", "content": e.dxf.name, "layer": e.dxf.layer})
        output_csv = dxf_path.replace(".dxf", "_extracted.csv")
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=["type", "content", "layer"])
            writer.writeheader()
            writer.writerows(results)
        return f"Success: Extracted {len(results)} items to {output_csv}"
    except Exception as e: return f"Error: {str(e)}"

@mcp.tool()
def process_door_schedule(dxf_path: str) -> str:
    """Extract and clean door schedules from a DXF file with page mapping."""
    BLACKLIST = ['TYPE', 'ADDITIONAL EQUIPMENT', 'AREA:', 'โล่ง', '200X200', '200X300', 'FD.', 'REF.', '-']
    def is_blacklisted(text):
        clean_text = text.strip().upper()
        return not clean_text or clean_text == '-' or any(item.upper() in clean_text for item in BLACKLIST)

    try:
        doc = ezdxf.readfile(dxf_path)
        layout_viewports = []
        for l in doc.layouts:
            if l.name.lower() == 'model': continue
            for vp in l.query('VIEWPORT'):
                if vp.dxf.id == 1: continue 
                vc = vp.dxf.view_center_point
                vh = vp.dxf.view_height
                vw = vh * (vp.dxf.width / vp.dxf.height)
                layout_viewports.append({
                    'layout': l.name, 'min_x': vc.x - vw/2, 'max_x': vc.x + vw/2, 'min_y': vc.y - vh/2, 'max_y': vc.y + vh/2
                })

        all_text = []
        for l in doc.layouts:
            if l.name.lower() == 'model': continue
            for e in l.query('TEXT MTEXT'):
                t = (e.dxf.text if e.dxftype() == 'TEXT' else e.text).strip()
                if not is_blacklisted(t): all_text.append({'Text': t, 'Page': l.name})
                    
        msp = doc.modelspace()
        for e in msp.query('TEXT MTEXT'):
            t = (e.dxf.text if e.dxftype() == 'TEXT' else e.text).strip()
            if not is_blacklisted(t):
                pos = getattr(e.dxf, 'insert', getattr(e.dxf, 'align_point', None))
                page = "Unknown"
                if pos:
                    for vp in layout_viewports:
                        if vp['min_x'] <= pos.x <= vp['max_x'] and vp['min_y'] <= pos.y <= vp['max_y']:
                            page = vp['layout']; break
                all_text.append({'Text': t, 'Page': page})

        output_csv = dxf_path.replace(".dxf", "_doors.csv")
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['Text', 'Page'])
            writer.writeheader(); writer.writerows(all_text)
        return f"Success: Processed {len(all_text)} entries to {output_csv}"
    except Exception as e: return f"Error: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
