months = int(input('Years: '))*12 #23*12
initial = float(input('Principal: ')) #300000
interest = float(input('Yearly Interest Rate: ')) #0.035

def is_viable(initial, monthly_rate, interest):
	return (initial-12*monthly_rate)*(1.0+interest) < initial

def months_to_pay(initial, monthly_rate, interest):
	months_elapsed = 0
	while(initial > 0.0):
		initial -= monthly_rate
		months_elapsed += 1
		if(months_elapsed % 12 == 3):
			initial += initial*interest
	return (months_elapsed, -initial)

def total_paid(initial, monthly_rate, interest):
	paid = 0
	months_elapsed = 0
	while(initial > 0.0):
		initial -= monthly_rate
		paid += monthly_rate
		months_elapsed += 1
		if(months_elapsed % 12 == 0):
			initial += initial*interest
	paid -= initial
	return paid

def guess_monthly_rate(initial, interest, months):
	eta = 100
	monthly_rate = 1000
	while(not is_viable(initial, monthly_rate, interest)):
		monthly_rate += eta
		eta *= 1.01
	guess_months, overshoot = months_to_pay(initial, monthly_rate, interest)
	while(guess_months != months) or (overshoot >= 0.001):
		if(guess_months > months):
			monthly_rate += eta
		elif(guess_months < months):
			monthly_rate -= eta
		else:
			monthly_rate -= eta
		guess_months, overshoot = months_to_pay(initial, monthly_rate, interest)
		eta *= 0.99
	return monthly_rate

monthly_rate = guess_monthly_rate(initial, interest, months)

print()
print('Monthly Rate: '+str(monthly_rate))
print('Total Paid (Exact): '+str(months*monthly_rate))
print('Total Paid (Approximate): '+str(total_paid(initial, monthly_rate, interest)))
print('Total Interest: '+str(months*monthly_rate-initial))
