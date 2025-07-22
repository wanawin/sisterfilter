import streamlit as st

st.title("Filter to Combos with Sister Matches")

st.markdown("""
Paste a list of 5-digit combos below (one per line or comma-separated).
This tool will keep only those combos that have at least one "sister" —
meaning the list includes both the previous (-1) and next (+1) combo in sequence.
""")

user_input = st.text_area("Paste your combos here:", height=300)

if user_input:
    raw_lines = user_input.replace(',', '\n').split('\n')
    combos = [line.strip() for line in raw_lines if line.strip().isdigit() and len(line.strip()) == 5]
    combo_set = set(combos)

    def get_neighbors(combo):
        """Return a list of sister neighbors by incrementing and decrementing by 1."""
        neighbors = []
        for i in range(5):
            digit = int(combo[i])
            for delta in [-1, 1]:
                new_digit = digit + delta
                if 0 <= new_digit <= 9:
                    new_combo = combo[:i] + str(new_digit) + combo[i+1:]
                    neighbors.append(new_combo)
        return neighbors

    # Keep combos that have both X-1 and X+1 neighbor(s) in the list
    sister_matches = []
    for combo in combos:
        neighbors = get_neighbors(combo)
        found_minus = any(n in combo_set for n in neighbors if int(n) < int(combo))
        found_plus  = any(n in combo_set for n in neighbors if int(n) > int(combo))
        if found_minus and found_plus:
            sister_matches.append(combo)

    sister_matches = sorted(set(sister_matches))

    st.success(f"Found {len(sister_matches)} combos with valid sister chains.")
    st.markdown("### Copyable Result")
    st.text("\n".join(sister_matches))

    st.download_button("Download .txt", "\n".join(sister_matches), file_name="sister_combos.txt")
