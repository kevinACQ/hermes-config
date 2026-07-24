#!/usr/bin/env python3
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

BASE = "https://api.retellai.com"
PROJECT = Path("/Users/kevin/projects/voice-onboarding-mvp")

def load_env(path):
    for raw in path.read_text().splitlines():
        s=raw.strip()
        if s and not s.startswith('#') and '=' in s:
            k,v=s.split('=',1)
            os.environ.setdefault(k, v.strip().strip('"').strip("'"))

def req(method, path, payload=None):
    data=None if payload is None else json.dumps(payload).encode()
    r=urllib.request.Request(BASE+path, data=data, method=method,
        headers={"Authorization": f"Bearer {os.environ['RETELL_API_KEY']}", "Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            body=resp.read().decode()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body=e.read().decode(errors='replace')
        raise RuntimeError(f"{method} {path} failed ({e.code}): {body[:1200]}")

def main():
    load_env(PROJECT/".env")
    dest=os.environ.get("DESTINATION_PHONE")
    if not dest: raise RuntimeError("DESTINATION_PHONE is required")
    prod_agent=req("GET", f"/get-agent/{os.environ['RETELL_AGENT_ID_HERMES']}")
    prod_llm=req("GET", f"/get-retell-llm/{os.environ['RETELL_LLM_ID_HERMES']}")
    temp_llm=temp_agent=call_id=None
    prompt="""You are Alex Hormozi calling TAO Asian Bistro at The Venetian in Las Vegas to make a simulated dinner reservation. The person answering is role-playing the restaurant host. Stay fully in character and never mention AI, testing, Retell, or simulation unless the other person explicitly ends the role-play.

Goal: request a reservation for 2 guests tonight, Friday July 24, 2026, at 7:00 PM under Kevin Gong. The venue is TAO Asian Bistro at The Venetian. Known Friday hours are 5:00 PM–11:30 PM. If 7:00 PM is unavailable, ask for and accept the nearest available time between 6:30 PM and 7:30 PM. Do not accept a time outside that range. If asked for a phone number, politely say you can provide it later and continue the role-play without inventing one. Do not invent availability, policies, fees, or a confirmation number. Confirm the agreed date, time, party size, and reservation name, then close naturally.

Sound like Alex Hormozi: direct, confident, concise, warm, and conversational. Use short turns and allow the host to lead the booking questions."""
    begin="Hi, I'd like to make a dinner reservation for two tonight at 7:00 PM, under Kevin Gong."
    try:
        llm_payload={
            "model": prod_llm.get("model") or "gpt-4.1-mini",
            "general_prompt": prompt,
            "begin_message": begin,
        }
        for k in ("model_temperature","model_high_priority","tool_call_strict_mode"):
            if k in prod_llm: llm_payload[k]=prod_llm[k]
        llm=req("POST","/create-retell-llm",llm_payload); temp_llm=llm["llm_id"]
        agent_payload={
            "agent_name":"TEMP Alex - TAO reservation roleplay",
            "voice_id": prod_agent.get("voice_id") or os.environ["RETELL_HERMES_VOICE_ID"],
            "response_engine":{"type":"retell-llm","llm_id":temp_llm},
        }
        for k in ("language","voice_model","voice_temperature","voice_speed","responsiveness","interruption_sensitivity","enable_backchannel","backchannel_frequency","reminder_trigger_ms","reminder_max_count","ambient_sound","ambient_sound_volume"):
            if k in prod_agent and prod_agent[k] is not None: agent_payload[k]=prod_agent[k]
        agent=req("POST","/create-agent",agent_payload); temp_agent=agent["agent_id"]
        call=req("POST","/v2/create-phone-call",{
            "from_number":os.environ["RETELL_PHONE_NUMBER"],
            "to_number":dest,
            "override_agent_id":temp_agent,
            "metadata":{"purpose":"TAO reservation roleplay","simulation":True,"recipient_alias":"Drew Thompson"}
        })
        call_id=call["call_id"]
        print(json.dumps({"event":"initiated","call_id":call_id,"status":call.get("call_status"),"recipient":"Drew Thompson"}), flush=True)
        deadline=time.time()+900
        final=None
        while time.time()<deadline:
            time.sleep(5)
            final=req("GET",f"/v2/get-call/{call_id}")
            status=final.get("call_status")
            if status in ("ended","error"):
                print(json.dumps({"event":"completed","call_id":call_id,"status":status,"disconnect_reason":final.get("disconnection_reason"),"duration_ms":final.get("duration_ms")}), flush=True)
                return
        print(json.dumps({"event":"timeout","call_id":call_id,"last_status":(final or {}).get("call_status")}), flush=True)
    finally:
        if temp_agent:
            try: req("DELETE",f"/delete-agent/{temp_agent}")
            except Exception as e: print(json.dumps({"cleanup_warning":"agent","error":str(e)}), file=sys.stderr)
        if temp_llm:
            try: req("DELETE",f"/delete-retell-llm/{temp_llm}")
            except Exception as e: print(json.dumps({"cleanup_warning":"llm","error":str(e)}), file=sys.stderr)

if __name__=="__main__":
    try: main()
    except Exception as e:
        print(json.dumps({"event":"error","error":str(e)}), file=sys.stderr)
        sys.exit(1)
