import pyzed.sl as sl

if __name__ == "__main__":
    # connection_18 = '['
    # for BODY_BONE in sl.BODY_BONES:
    #     # MATLAB INDEX
    #     connection_18 += str(BODY_BONE[0].value+1) + ' ' + str(BODY_BONE[1].value+1) + ';'
    # connection_18 = connection_18[:-1]
    # connection_18 += ']'
    # print(connection_18)
    # joints_18 = '['
    # for BODY_PART in list(sl.BODY_PARTS):
    #     joints_18 += '\"'+BODY_PART.name+ '\",'
    # joints_18 = joints_18[:-1]
    # joints_18 += ']'
    # print(joints_18)
    connection_34 = '['
    for BODY_BONE in sl.BODY_BONES_POSE_34:
        # MATLAB INDEX
        connection_34 += str(BODY_BONE[0].value+1) + \
            ' ' + str(BODY_BONE[1].value+1) + ';'
    connection_34 = connection_34[:-1]
    connection_34 += ']'
    print(connection_34)
    joints_34 = '['
    for BODY_PART in list(sl.BODY_PARTS_POSE_34):
        joints_34 += '\"'+BODY_PART.name + '\",'
    joints_34 = joints_34[:-1]
    joints_34 += ']'
    print(joints_34)
