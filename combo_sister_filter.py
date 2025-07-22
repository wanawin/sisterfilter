import streamlit as st

st.title("Filter to Combos with Sister Matches")

st.markdown("""
Paste a list of 5-digit combos below (one per line or comma-separated).
This tool will:
- Prioritize combos with **at least two ±1 digit neighbors**.
- Also return a separate section for combos with **at least two ±2 digit neighbors** (if no ±1 match).
""")

user_input = st.text_area("Paste your combos here:", height=300)

if user_input:
    raw_lines = user_input.replace(',', '\n').split('\n')
    combos = [line.strip() for line in raw_lines if line.strip().isdigit() and len(line.strip()) == 5]
    combo_set = set(combos)

    def get_neighbors(combo, step):
        """Return a list of neighbors by incrementing and decrementing digits by step."""
        neighbors = []
        for i in range(5):
            digit = int(combo[i])
            for delta in [-step, step]:
                new_digit = digit + delta
                if 0 <= new_digit <= 9:
                    new_combo = combo[:i] + str(new_digit) + combo[i+1:]
                    neighbors.append(new_combo)
        return neighbors

    priority_matches = []
    secondary_matches = []

    for combo in combos:
        neighbors1 = get_neighbors(combo, 1)
        cluster1 = [n for n in neighbors1 if n in combo_set]

        if len(cluster1) >= 2:
            priority_matches.append(combo)
        else:
            neighbors2 = get_neighbors(combo, 2)
            cluster2 = [n for n in neighbors2 if n in combo_set]
            if len(cluster2) >= 2:
                secondary_matches.append(combo)

    priority_matches = sorted(set(priority_matches))
    secondary_matches = sorted(set(secondary_matches) - set(priority_matches))

    total_found = len(priority_matches) + len(secondary_matches)
    st.success(f"Found {total_found} combos with valid sister chains.")

    if priority_matches:
        st.markdown("### Primary Sister Matches (±1)")
        st.text("\n".join(priority_matches))
        st.download_button("Download Primary (±1) .txt", "\n".join(priority_matches), file_name="primary_sister_combos.txt")

    if secondary_matches:
        st.markdown("### Secondary Sister Matches (±2 only)")
        st.text("\n".join(secondary_matches))
        st.download_button("Download Secondary (±2) .txt", "\n".join(secondary_matches), file_name="secondary_sister_combos.txt")
