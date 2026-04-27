# 🏗️ Takon MCP Core
### Model Context Protocol (MCP) Server for Construction & Engineering Management

ชุดเครื่องมือ MCP Server ระดับมืออาชีพสำหรับงานบริหารงานก่อสร้างและวิศวกรรม ออกแบบมาเพื่อให้ AI Agent (Claude, thClaws, Cursor) สามารถลงมือทำงานกับไฟล์ในเครื่อง (CAD, Excel, Photos) ได้จริง

---

## 🌟 จุดเด่น (Highlights)
- **Modular Design**: แยกโมดูลงานก่อสร้าง (Construction) และงานวิศวกรรม (CAD) ออกจากกัน เพื่อความเบาและประสิทธิภาพสูงสุด
- **Hybrid AI Architecture**: สลับการทำงานระหว่าง **Cloud API** (Typhoon, OpenAI) และ **Local AI** (รัน Moondream ในเครื่อง 100% สำหรับการอ่านรูปภาพ)
- **Agnostic AI**: รองรับการเชื่อมต่อกับ AI ทุกค่ายที่ใช้มาตรฐาน OpenAI-compatible API (รวมถึง Ollama และ Qwen)
- **FastMCP Powered**: พัฒนาด้วยมาตรฐานล่าสุดของ Anthropic มั่นใจได้ในเรื่องความเสถียรและความแม่นยำของ Tool Schema

---

## 🛠️ เครื่องมือที่มีให้ใช้งาน (Tools)

### 1. 📊 โมดูลงานก่อสร้าง (`takon-construction`)
- `generate_daily_report`: สร้างรายงานประจำวัน Excel พร้อมวิเคราะห์รูปภาพหน้างานอัตโนมัติ
- `generate_project_dashboard`: สร้าง Dashboard HTML สรุปภาพรวมโครงการด้วย AI Insight

### 2. 📐 โมดูลงานวิศวกรรม (`takon-cad`)
- `extract_dxf_data`: สกัดข้อมูล Text และ Block จากไฟล์ CAD (.dxf) ออกมาเป็น CSV
- `process_door_schedule`: สกัดและทำความสะอาดข้อมูลแบบขยายประตู พร้อมเชื่อมโยงเลขหน้าอัตโนมัติ

---

## ⚙️ การตั้งค่า AI (Configuration)

คุณสามารถสลับโหมดการทำงานของ AI ได้ผ่าน `env` ในไฟล์ตั้งค่า:

### 🏠 โหมดรันในเครื่อง (Local Vision AI)
ใช้ Moondream ในการวิเคราะห์รูปภาพโดยไม่ต้องต่อเน็ต:
```json
"env": { "AI_STRATEGY": "local" }
```

### ☁️ โหมดใช้ Cloud API (Typhoon/OpenAI)
```json
"env": {
  "AI_STRATEGY": "api",
  "AI_BASE_URL": "https://api.opentyphoon.ai/v1",
  "AI_API_KEY": "YOUR_KEY",
  "AI_VISION_MODEL": "typhoon-ocr",
  "AI_TEXT_MODEL": "typhoon-v2.1-12b-instruct"
}
```

---

## 📦 วิธีการติดตั้ง (Installation)

### 1. สำหรับ thClaws (Tauri/Rust version)
thClaws รองรับการติดตั้งแบบ Plugin โดยตรง:
- พิมพ์คำสั่งในหน้าแชท:
  ```bash
  /plugin install https://github.com/PRIDA-TAKON/takon_mcp_core
  ```
- **หรือติดตั้งแบบรันสคริปต์ในเครื่อง:** คลิกขวาที่ไฟล์ `install_mcp.ps1` แล้วเลือก **Run with PowerShell**

### 2. สำหรับ Claude Desktop
ก๊อปปี้ไปวางใน `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "takon-construction": {
      "command": "uv",
      "args": ["--directory", "PATH_TO_PROJECT", "run", "takon-construction"],
      "env": { "AI_STRATEGY": "local" }
    }
  }
}
```

---

## 📂 โครงสร้างโปรเจค (Project Structure)
- `src/takon_mcp_core/construction.py`: เครื่องมือจัดการรายงานและ Dashboard
- `src/takon_mcp_core/cad.py`: เครื่องมือจัดการไฟล์ CAD/DXF
- `plugin.json` / `manifest.json`: ไฟล์สำหรับติดตั้งใน thClaws
- `AGENTS.md`: คำแนะนำพฤติกรรมสำหรับ AI Agent
- `install_mcp.ps1`: สคริปต์ติดตั้งอัตโนมัติสำหรับ Windows

---
*Created with ❤️ by Takon (PRIDA-TAKON) - มาตรฐานใหม่เพื่อวิศวกรไทย*
