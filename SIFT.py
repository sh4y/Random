def generateOctaveLayer(octave_layer, s, sigma, mod_start):
    print 'Initial Sigma: ' + str(sigma)
    modifier = mod_start
    k = sqrt(2)
    octave = []
    sigmas = []
    for x in range(s + 3):
        ksig = (k ** modifier) * sigma
        print ksig
        if len(octave) == 0:
            img = octave_layer
        else:
            img = octave[-1]
        scale = ndimage.gaussian_filter(img, sigma = ksig)
        sigmas.append(ksig)
        octave.append(scale)
        modifier += 1
    return octave, sigmas

def generateOctavePyramid(img, p, s, sigma):
    pyramid = []
    sigmas = []
    for x in range(p):
        octave, moddedSigmas = generateOctaveLayer(img, s, sigma, x)
        sigmas.append(moddedSigmas)
        pyramid.append(octave)
        sigma = sigmas[-1][1]
        img = octave[-3][::2,::2]  #get third last octave, + all corresponding layers to it, skipping every 2
    return pyramid,sigmas

def generateDoG(octave):
    dog = []
    for i in range(1, len(octave)):
        dog.append(octave[i] - octave[i-1])
    result = np.stack(dog, axis=2)
    return result

def generateDoGPyramid(pyr):
    dog = []
    for octave in pyr:
        diffGauss = generateDoG(octave)
        #print diffGauss.shape
        dog.append(diffGauss)
    return dog

def findKeypoints(dogs):
    patch_size = 16
    offset = (patch_size // 2)
    octave_num = 0
    print 'Offset: ' + str(offset)
    keypoints = {}
    for dog in dogs:
        print dog.shape
        for x in range(offset+1, dog.shape[0]-offset+1):
            for y in range(offset, dog.shape[1]-offset+1):
                for z in range(1, dog.shape[2]-1):
                    prism = dog[x-1:x+2,y-1:y+2,z-1:z+2]
                    #check if point is max in prism
                    value = dog[x][y][z]
                    is_max = prism.max() == value and value > 0
                    if is_max and value < 0.8 and value > 0:
                        if octave_num in keypoints:
                            keypoints[octave_num].append((x, y, z))
                        else:
                            keypoints[octave_num] = [(x, y, z)]
        octave_num += 1
    return keypoints
