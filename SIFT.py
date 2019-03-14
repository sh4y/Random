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
