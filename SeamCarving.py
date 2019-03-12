def seamCarve(file):
    fileCopy = np.copy(file).reshape((file.shape[0], file.shape[1], 3))

    for count in range(100):
        argmin_list = []
        h, v, mag = compute_gradient(fileCopy)
        #print mag.shape
        red_channel = np.array([], dtype='uint8')
        green_channel = np.array([], dtype='uint8')
        blue_channel = np.array([], dtype='uint8')
        min_value = np.min(mag[0])
        minIndices = [i for i, x in enumerate(mag[0]) if x == min_value]
        x = random.choice(minIndices)
        #print 'Randomly starting at: ' + str(x)
        for y in range(mag.shape[0]-1):
            neighbours = []
            if (x - 1 >= 0):
                neighbours.append(mag[y+1][x+1])
            else:
                neighbours.append(256)

            neighbours.append(mag[y][x + 1])

            if (x + 1 < mag.shape[0]):
                neighbours.append(mag[y+1][x-1])
            else:
                neighbours.append(256)
            neighbour_offset = np.argmin(neighbours) - 1
            argmin_list.append(x)
            #todo: delete the fucking elements

            x = x + neighbour_offset
        argmin_list.append(x)
        #print 'Appended all neighbours'
        #print 'Number of entries in argmin: ' + str(len(argmin_list))
        #show_seam(file, argmin_list)
        #print 'fc shape: ' + str(fileCopy.shape)
        for row in range(mag.shape[0]):
            for color in range(3):
                channel = fileCopy[:,:,color]
                deleted_channel_row = np.delete(channel[row], argmin_list[row])
                if color == 0:
                    red_channel = np.concatenate([red_channel, deleted_channel_row])
                elif color == 1:
                    green_channel = np.concatenate([green_channel, deleted_channel_row])
                else:
                    blue_channel = np.concatenate([blue_channel, deleted_channel_row])
        #print red_channel.shape
        #mag.shape[0], mag.shape[1]-1
        red_channel = np.reshape(red_channel, (red_channel.shape[0], 1))
        green_channel = np.reshape(green_channel, (red_channel.shape[0], 1))
        blue_channel = np.reshape(blue_channel, (red_channel.shape[0], 1))
        #new_img = np.reshape([red_channel, green_channel, blue_channel], (file.shape[0], file.shape[1]-1, 3))
        #deletedImage = np.dstack((red_channel, green_channel, blue_channel))
        red = Image.fromarray(red_channel)
        green = Image.fromarray(green_channel)
        blue = Image.fromarray(blue_channel)
        #new_img = np.reshape([red_channel, green_channel, blue_channel], (file.shape[0], file.shape[1]-1, 3))
        deletedImage = np.asarray(Image.merge("RGB", (red, green,blue)))
        fileCopy = np.reshape(deletedImage, (fileCopy.shape[0], fileCopy.shape[1] - 1, 3))
    f, axarr = plt.subplots(1,2)
    axarr[0].axis('off')
    axarr[0].imshow(file)
    axarr[1].imshow(fileCopy)
    plt.axis('off')
    plt.show()
    return fileCopy.shape
