import streamlit as st
import random

pairings = {
        8: [
            [(0, 4), (1, 5), (2, 6), (3, 7)],
            [(0, 5), (1, 6), (2, 7), (3, 4)],
            [(0, 6), (1, 7), (2, 4), (3, 5)],
            [(0, 7), (1, 4), (2, 5), (3, 6)],
            [(0, 1), (2, 3), (4, 5), (6, 7)],
            [(0, 2), (1, 3), (4, 6), (5, 7)],
            [(0, 3), (1, 2), (4, 7), (5, 6)]
        ],
        9: [
            [(0, 4), (1, 5), (2, 6), (3, 7)],
            [(0, 5), (1, 6), (2, 7), (3, 8)],
            [(0, 6), (1, 7), (2, 8), (3, 4)],
            [(0, 7), (1, 8), (2, 4), (3, 5)],
            [(0, 8), (1, 4), (2, 5), (3, 6)],
            [(0, 1), (2, 3), (4, 5), (6, 7)],
            [(0, 2), (1, 3), (4, 6), (5, 7)],
            [(0, 3), (1, 2), (4, 7), (5, 8)],
            [(0, 1), (2, 3), (4, 5), (6, 8)]
        ],
        10: [ (1, 2), (3, 4), (5, 6), (7, 8)], 
        [ (9, 1), (10, 5), (4, 2), (3, 6)],
        [ (7, 1), (8, 4), (3, 2), (10, 9)],
        [ (9, 8), (10, 2), (7, 6), (5, 1)],
        [(3, 9), (5, 7), (4, 10), (6, 8)],
        [ (1, 4), (9, 6), (3, 7), (5, 8)],
        [ (1, 3), (7, 2), (4, 10), (9, 6)],
        [ (1, 10), (5, 9), (8, 3), (2, 6)],
        [ (1, 8), (10, 4), (2, 5), (9, 7)],
        [ (2, 3), (5, 10),(7,8),(6,4)],
        ],
        11: [
            [(0, 6), (1, 7), (2, 8), (3, 9)],
            [(4, 10), (0, 7), (6, 8), (1, 9)],
            [(2, 10), (4, 5), (0, 8), (7, 9)],
            [(6, 10), (2, 5), (3, 4), (0, 9)],
            [(8, 10), (6, 5), (1, 4), (2, 3)],
            [(0, 10), (8, 5), (7, 4), (6, 3)],
            [(1, 2), (10, 5), (9, 4), (8, 3)],
            [(7, 2), (8, 1), (0, 5), (10, 3)],
            [(9, 2), (8, 6), (7, 1), (0, 4)],
            [(5, 3), (10, 1), (9, 6), (8, 7)],
            [(0, 3), (4, 2), (5, 1), (6, 7)]
        ],
        12: [
            [(0, 6), (1, 7), (2, 8), (3, 9)],
            [(4, 10), (5, 11), (0, 7), (6, 8)],
            [(1, 9), (2, 10), (3, 11), (4, 5)],
            [(0, 8), (7, 9), (6, 10), (1, 11)],
            [(2, 5), (3, 4), (0, 9), (8, 10)],
            [(7, 11), (6, 5), (1, 4), (2, 3)],
            [(0, 10), (9, 11), (8, 5), (7, 4)],
            [(6, 3), (1, 11), (10, 5), (9, 4)],
            [(8, 2), (7, 1), (10, 4), (9, 3)],
            [(0, 5), (11, 4), (10, 2), (1, 3)],
            [(8, 6), (7, 5), (0, 4), (11, 3)],
            [(10, 6), (9, 5), (11, 2), (8, 7)]
        ]
    }

def get_matches(participants):
    num_participants = len(participants)
    if num_participants in pairings:
        rounds = pairings[num_participants]
        all_matches = []
        for round in rounds:
            round_matches = []
            match1 = [round[0], round[1]]
            #random.shuffle(match1)
            #random.shuffle(match1)
            match2 = [round[2], round[3]]
            #random.shuffle(match2)
            #random.shuffle(match2)
            round_matches.append((participants[match1[0][0]], participants[match1[0][1]], participants[match1[1][0]], participants[match1[1][1]]))
            round_matches.append((participants[match2[0][0]], participants[match2[0][1]], participants[match2[1][0]], participants[match2[1][1]]))
            all_matches.append(round_matches)
        return all_matches
    else:
        return None

# Streamlit interface for the tournament creator
st.title("Oliver's RR Tournament Creator")
names_input = st.text_input("Enter participant names, comma-separated (8-12) - They are automatically randomized")

if names_input:
    if 'participants' not in st.session_state or st.session_state['input'] != names_input:
        # Update the session state for participants
        participants = [name.strip().capitalize() for name in names_input.split(',')]
        #random.shuffle(participants)  # Randomize the list of participants
        st.session_state['participants'] = participants
        st.session_state['input'] = names_input  # Store the current input to compare later
        st.session_state['matches'] = get_matches(participants)  # Initialize matches and store

        # Reset session state data related to participants
        st.session_state['wins'] = {name: 0 for name in st.session_state['participants']}
        st.session_state['tiebreakers'] = {name: 0 for name in st.session_state['participants']}

    if len(st.session_state['participants']) in pairings:
        matches = st.session_state['matches']
        if matches:
            colors = ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845']
            results = {"wins": {}, "tiebreakers": {}}
            for name in st.session_state['participants']:
                results['wins'][name] = 0
                results['tiebreakers'][name] = 0
            for i, round in enumerate(matches, 1):
                color = colors[i % len(colors)]
                st.markdown(f"<h2 style='color: {color};'>Round {i}</h2>", unsafe_allow_html=True)
                score_inputs = []
                for j, match in enumerate(round, 1):
                    if j%2 == 0:
                        st.write("Court 2:", match[0] + " & " + match[1], " vs ", match[2] + " & " + match[3])
                    else:
                        st.write("Court 1:", match[0] + " & " + match[1], " vs ", match[2] + " & " + match[3])
                    with st.container():
                        col1, col2 = st.columns(2)
                        with col1:
                            team1_score = st.number_input(f"Score for {match[0]} & {match[1]}", min_value=0, key=f"{i}_{j}_team1_score")
                        with col2:
                            team2_score = st.number_input(f"Score for {match[2]} & {match[3]}", min_value=0, key=f"{i}_{j}_team2_score")
                        score_inputs.append((match, team1_score, team2_score))

                for match, team1_score, team2_score in score_inputs:
                    if team1_score > team2_score:
                        results['wins'][match[0]] += 1
                        results['wins'][match[1]] += 1
                        results['tiebreakers'][match[2]] += team2_score
                        results['tiebreakers'][match[3]] += team2_score
                    elif team2_score > team1_score:
                        results['wins'][match[2]] += 1
                        results['wins'][match[3]] += 1
                        results['tiebreakers'][match[0]] += team1_score
                        results['tiebreakers'][match[1]] += team1_score

                st.session_state['scoreResult'] = results

# Sidebar for tally of scores and determining the winner
with st.sidebar:

    st.header("Leaderboard:")
    if 'participants' in st.session_state:
        results = [(name, st.session_state["scoreResult"]['wins'].get(name, 0), st.session_state["scoreResult"]['tiebreakers'].get(name, 0)) for name in st.session_state['participants']]
        results.sort(key=lambda x: (-x[1], -x[2]))

        for name, wins, tiebreakers in results:
            st.write(f"{name}: {wins} wins, Tiebreakers: {tiebreakers}")

        # Determine the winner
        if results:
            winner = results[0][0]
            max_wins, max_tiebreakers = results[0][1], results[0][2]
            for r in results[1:]:
                if r[1] == max_wins and r[2] > max_tiebreakers:
                    winner = r[0]
                    max_tiebreakers = r[2]
                elif r[1] < max_wins:
                    break

            st.subheader("Winner:")
            st.success(f"{winner}")
    else:
        st.write("Enter participant names to see the score tally.")
