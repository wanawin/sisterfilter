import streamlit as st

st.title("Filter to Combos with Sister Matches")

st.markdown("""
Paste a list of 5-digit combos below (one per line or comma-separated).
This tool will keep only those combos that have at least one "sister" —
meaning another combo in the list that differs by exactly ±1 or ±2 in exactly one digit.
""")

user_input = st.text_area("Paste your combos here:", height=300)

if user_input:
    raw_lines = user_input.replace(',', '\n').split('\n')
    combos = [line.strip() for line in raw_lines if line.strip().isdigit() and len(line.strip()) == 5]
    combo_set = set(combos)

    def is_sister(a, b):
        diff = 0
        for i in range(5):
            if a[i] != b[i]:
                if abs(int(a[i]) - int(b[i])) in (1, 2):
                    diff += 1
                else:
                    return False
        return diff == 1

    sister_matches = set()
    for i, a in enumerate(combos):
        for j in range(i + 1, len(combos)):
            b = combos[j]
            if is_sister(a, b):
                sister_matches.add(a)
                sister_matches.add(b)

    sister_matches = sorted(sister_matches)

    st.success(f"Found {len(sister_matches)} combos with at least one sister.")
    st.markdown("### Copyable Result")
    st.text("\n".join(sister_matches))

    st.download_button("Download .txt", "\n".join(sister_matches), file_name="sister_combos.txt")
