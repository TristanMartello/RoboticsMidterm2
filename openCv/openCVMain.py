import requests

# Function for eliminating white noise in the background of photos and amplifying images of a certain color
def oneColorTest(goal, other1, other2, diffVal, thresh):
    sum = 0
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            if goal[i][j] > diffVal and (other1[i][j] > diffVal or other2[i][j] > diffVal):
                goal[i][j] = 0
            elif goal[i][j] > thresh:
                goal[i][j] = 255
                sum += 1
    return goal, sum

# Take the image and split it into r,g,b, values
cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
b,g,r = cv2.split(cv2_image)
b2, g2, r2 = cv2.split(cv2_image)
b3, g3, r3 = cv2.split(cv2_image)
grey = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2GRAY)
cam.show(grey)  # shows any cv2 image in the same spot on the webpage (third image)

# Set threshhold values and run the color isolation algorithm
diffVal = 80
thresh = 90
#display(Image.fromarray(diff))
diffR, sumR = oneColorTest(r, g, b, diffVal, thresh)
diffG, sumG = oneColorTest(g2, r2, b2, diffVal, thresh)
diffB, sumB = oneColorTest(b3, g3, r3, diffVal, thresh)

# Display the color counts, and determine the most prominent color
print(sumR, sumG, sumB)
if sumR > sumG and sumR > sumB:
    itemColor = "Red"
elif sumG > sumR and sumG > sumB:
    itemColor = "Green"
elif sumB > sumR and sumB > sumG:
    itemColor = "Blue"
else:
    itemColor = "No clear color"

# Print the observed colors, display the images
print("Color:", itemColor)                   
display(Image.fromarray(diffR))
display(Image.fromarray(diffG))
display(Image.fromarray(diffB))

# If the right colors are identified, update the airtable value
if itemColor == "Red" or itemColor == "Green":
    base_url = "https://api.airtable.com/v0/app2LMuREL2bqnlFC/Tasks"
    api_key = "patCqHYMHGA7KjBlh.69c79325987681970b3118dee9a291c4feb8a3fb68255f609cfa6d861ba81a14"
    
    # Specify the record ID you want to update
    record_id = "recSMjN1cKHiKaYxf"
    
    # Set the headers, including the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",}
    
    # Define the data to be updated. For example, to update the 'color' field:
    data = {"fields": {"Value": itemColor}}
    
    try:
        update_url = f"{base_url}/{record_id}"
        response = requests.patch(update_url, headers=headers, json=data)
        response.raise_for_status()  # Check for HTTP status code errors
    
        updated_record = response.json()
        print("Updated Record:", updated_record)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    

                
#oldthresh, diffThresh = cv2.threshold(diff,diffVal,255,cv2.THRESH_BINARY)

textBox.innerText=repr(np.sum(grey))
