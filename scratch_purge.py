import re

def purge_emr_from_vip_cases():
    with open('src/screens/doctor/VIPCases.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Import useNavigate
    content = content.replace(
        'import React, { useState, useEffect, useCallback } from "react";',
        'import React, { useState, useEffect, useCallback } from "react";\nimport { useNavigate } from "react-router-dom";'
    )

    # Remove PatientEMRModal import
    content = content.replace(
        'import PatientEMRModal from "../../components/common/PatientEMRModal";\n',
        ''
    )

    # Add navigate hook
    content = content.replace(
        'const { token } = useAuthStore();',
        'const { token } = useAuthStore();\n  const navigate = useNavigate();'
    )

    # 2. Purge state (active, history, etc.)
    # We will use regex to remove these lines
    states_to_remove = [
        r'const \[active, setActive\] = useState\(null\);\n',
        r'const \[activeTab, setActiveTab\] = useState\("orders"\);.*\n',
        r'const \[selectedServices, setSelectedServices\] = useState\(\[\]\);\n',
        r'const \[prescriptionItems, setPrescriptionItems\] = useState\(\[\]\);\n',
        r'const \[history, setHistory\] = useState\(\[\]\);\n',
        r'const \[historyLoading, setHistoryLoading\] = useState\(false\);\n',
        r'\s*// EMR Active Tab\s*\n',
        r'\s*// Services cart \(reset on patient select\)\s*\n',
        r'\s*// Patient History\s*\n'
    ]
    for state_pattern in states_to_remove:
        content = re.sub(state_pattern, '', content)

    # 3. Rewrite handleSelectPatient and purge EMR functions
    # Let's find the start of handleSelectPatient
    start_idx = content.find('  const handleSelectPatient = async (visit) => {')
    if start_idx == -1:
        # Maybe it's not async?
        start_idx = content.find('  const handleSelectPatient =')

    # Find the end of getCompletedResults (or just before the return statement)
    end_idx = content.find('  return (\n    <div className="space-y-6" dir="rtl">')
    
    if start_idx != -1 and end_idx != -1:
        new_methods = """  const handleSelectPatient = (visit) => {
    navigate('/doctor/queue', { state: { autoOpenVisitId: visit.visitId } });
  };

"""
        content = content[:start_idx] + new_methods + content[end_idx:]

    # 4. Remove PatientEMRModal from JSX
    # It's at the end of the return block:
    modal_regex = r'<PatientEMRModal[\s\S]*?/>'
    content = re.sub(modal_regex, '', content)

    with open('src/screens/doctor/VIPCases.js', 'w', encoding='utf-8') as f:
        f.write(content)

purge_emr_from_vip_cases()
