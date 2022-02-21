# This file is used to construct services.log appearance
printf "=%.0s"  $(seq 1 63) && echo  # Creates a divider
date  # Shows datetime
printf "=%.0s"  $(seq 1 63) && echo
echo  # Blank line
python3 /app/update_episodes.py  # Run script
echo
echo

