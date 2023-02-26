import pyzed.sl as sl

if __name__ == "__main__":
    connection = '['
    for BODY_BONE in sl.BODY_BONES:
        # MATLAB INDEX
        connection += str(BODY_BONE[0].value+1) + ' ' + str(BODY_BONE[1].value+1) + ';'
    connection += ']'
    print(connection)