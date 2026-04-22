import json
import re

def parse_llm_output(output):
    try:
        return json.loads(output)

    except:
        # 🔥 Extract ONLY JSON block
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if match:
            json_str = match.group()

            try:
                return json.loads(json_str)
            except Exception as e:
                print("⚠️ JSON still invalid:", json_str)
                return None

        print("⚠️ No JSON found in output")
        return None