import streamlit as st

st.title("Filter to Combos with Sister Matches")

st.markdown("""
Paste a list of 5-digit combos below (one per line or comma-separated).
This tool will keep combos that have:
- At least two neighbors that differ by ±1 in any **one** digit position (sister cluster).
- Optionally include those with two neighbors that differ by ±2 if no ±1 cluster is found.
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

    sister_matches = []
    for combo in combos:
        neighbors1 = get_neighbors(combo, 1)
        cluster1 = [n for n in neighbors1 if n in combo_set]

        if len(cluster1) >= 2:
            sister_matches.append(combo)
        else:
            neighbors2 = get_neighbors(combo, 2)
            cluster2 = [n for n in neighbors2 if n in combo_set]
            if len(cluster2) >= 2:
                sister_matches.append(combo)

    sister_matches = sorted(set(sister_matches))

    st.success(f"Found {len(sister_matches)} combos with valid sister chains.")
    st.markdown("### Copyable Result")
    st.text("\n".join(sister_matches))

    st.download_button("Download .txt", "\n".join(sister_matches), file_name="sister_combos.txt")
