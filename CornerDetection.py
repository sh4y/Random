def harris(img, threshold, alpha):
    gray_img = sk.color.rgb2grey(img)
    #smoothed_image = ndimage.convolve(gray_img, gaussian)
    Ix, Iy, mag = compute_gradient(gray_img, False)
    #Ix = ndimage.sobel(gray_img, axis=0)
    #Iy = ndimage.sobel(gray_img, axis=1)
    Ix2 = np.square(Ix)
    Iy2 = np.square(Iy)
    Ixy = np.multiply(Ix, Iy)
    print 'Computed image gradients'
    Mx = ndimage.gaussian_filter(Ix2, sigma=1.0)
    My = ndimage.gaussian_filter(Iy2, sigma=1.0)
    Mxy = ndimage.gaussian_filter(Ixy, sigma=1.0)
    print 'Computed M matrices'
    #3x3 sliding window
    ws = 4
    #ws/2 direction left and right
    corners = {}
    modifier = int(np.floor(ws / 2))
    suppression_matrix = np.zeros(gray_img.shape)
    for y in range(modifier, int(gray_img.shape[0]-modifier)):
        for x in range(modifier, int(gray_img.shape[1]-modifier)):
            IxWindow = Mx[y-modifier:y+modifier+1, x-modifier:x+modifier+1]
            IyWindow = My[y-modifier:y+modifier+1, x-modifier:x+modifier+1]
            IxyWindow = Mxy[y-modifier:y+modifier+1, x-modifier:x+modifier+1]
            sumIx = IxWindow.sum()
            sumIy = IyWindow.sum()
            sumIxy = IxyWindow.sum()
            det = (sumIx * sumIy) - np.square(sumIxy) #np.det doesnt handle this...
            R = det - alpha * np.square(sumIx + sumIy)
            #if R over threshold, add it to dict
            corners[(x,y)] = R
            suppression_matrix[y][x] = R
    for y in range(1, suppression_matrix.shape[0]-1):
        for x in range(1, suppression_matrix.shape[1]-1):
            neighbours = []
            neighbours.append(suppression_matrix[y][x-1])
            neighbours.append(suppression_matrix[y][x+1])
            neighbours.append(suppression_matrix[y+1][x])
            neighbours.append(suppression_matrix[y-1][x])
            neighbours.append(suppression_matrix[y+1][x+1])
            neighbours.append(suppression_matrix[y-1][x-1])
            neighbours.append(suppression_matrix[y+1][x-1])
            neighbours.append(suppression_matrix[y-1][x+1])
            if suppression_matrix[y][x] <= max(neighbours):
                if (x,y) in corners: corners.pop((x,y))
    cornersCopy = corners.copy()
    for item in cornersCopy:
        if cornersCopy[item] <= threshold:
            corners.pop(item)
    return corners

def showHarris():
    corners = harris(pic, 0.03, 0.06)
    plt.imshow(pic)
    print len(corners.keys())
    x, y = zip(*corners.keys())
    plt.scatter(x, y, s=5, c='red')
    plt.show()

showHarris()
