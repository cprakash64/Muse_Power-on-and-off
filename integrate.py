alpha_threshold = 100  # Example threshold

if np.mean(filtered_data) > alpha_threshold:
    b.set_light('Your Light Name', 'on', True)
else:
    b.set_light('Your Light Name', 'on', False)
