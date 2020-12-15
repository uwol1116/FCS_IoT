.class public Lcom/android/server/pm/checkCert;
.super Ljava/lang/Object;
.source "checkCert.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 15
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static byteArrayToHex([B)Ljava/lang/String;
    .locals 6
    .param p0, "bytes"    # [B

    .line 60
    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    .line 61
    .local v0, "result":Ljava/lang/StringBuffer;
    array-length v1, p0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_0

    aget-byte v3, p0, v2

    .local v3, "b":B
    and-int/lit16 v4, v3, 0xff

    add-int/lit16 v4, v4, 0x100

    const/16 v5, 0x10

    invoke-static {v4, v5}, Ljava/lang/Integer;->toString(II)Ljava/lang/String;

    move-result-object v4

    const/4 v5, 0x1

    invoke-virtual {v4, v5}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v0, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    .end local v3    # "b":B
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 62
    :cond_0
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    return-object v1
.end method

.method static compareWhitelist([Landroid/content/pm/Signature;)I
    .locals 11
    .param p0, "sigs"    # [Landroid/content/pm/Signature;

    .line 18
    const/4 v0, 0x0

    .line 20
    .local v0, "i":I
    const/4 v1, 0x0

    .line 21
    .local v1, "certSignature":Landroid/content/pm/Signature;
    const/4 v2, 0x0

    .line 22
    .local v2, "msgDigest":Ljava/security/MessageDigest;
    const/4 v3, 0x0

    .line 24
    .local v3, "cert":Ljava/lang/String;
    const/4 v4, 0x0

    aget-object v1, p0, v4

    .line 27
    :try_start_0
    const-string v5, "SHA256"

    invoke-static {v5}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;

    move-result-object v5

    move-object v2, v5

    .line 28
    invoke-virtual {v1}, Landroid/content/pm/Signature;->toByteArray()[B

    move-result-object v5

    invoke-virtual {v2, v5}, Ljava/security/MessageDigest;->update([B)V

    .line 29
    invoke-virtual {v2}, Ljava/security/MessageDigest;->digest()[B

    move-result-object v5

    invoke-static {v5}, Lcom/android/server/pm/checkCert;->byteArrayToHex([B)Ljava/lang/String;

    move-result-object v5
    :try_end_0
    .catch Ljava/security/NoSuchAlgorithmException; {:try_start_0 .. :try_end_0} :catch_0

    move-object v3, v5

    .line 32
    goto :goto_0

    .line 30
    :catch_0
    move-exception v5

    .line 31
    .local v5, "e":Ljava/security/NoSuchAlgorithmException;
    invoke-virtual {v5}, Ljava/security/NoSuchAlgorithmException;->printStackTrace()V

    .line 34
    .end local v5    # "e":Ljava/security/NoSuchAlgorithmException;
    :goto_0
    const-string v5, "FCS_IOT"

    invoke-static {v5, v3}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 38
    :try_start_1
    new-instance v6, Ljava/io/File;

    const-string v7, "/data/misc/pmwhitelist"

    invoke-direct {v6, v7}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 39
    .local v6, "file":Ljava/io/File;
    new-instance v7, Ljava/io/FileReader;

    invoke-direct {v7, v6}, Ljava/io/FileReader;-><init>(Ljava/io/File;)V

    .line 40
    .local v7, "filereader":Ljava/io/FileReader;
    new-instance v8, Ljava/io/BufferedReader;

    invoke-direct {v8, v7}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V

    .line 41
    .local v8, "bufReader":Ljava/io/BufferedReader;
    const-string v9, ""

    .line 42
    .local v9, "line":Ljava/lang/String;
    :cond_0
    invoke-virtual {v8}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;

    move-result-object v10

    move-object v9, v10

    if-eqz v10, :cond_1

    .line 44
    invoke-virtual {v3, v9}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v10

    if-eqz v10, :cond_0

    .line 45
    const-string v10, "find hash in whitelist"

    invoke-static {v5, v10}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 46
    const/4 v4, 0x1

    return v4

    .line 49
    :cond_1
    const-string v10, "can\'t find hash in whitelist"

    invoke-static {v5, v10}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    :try_end_1
    .catch Ljava/io/FileNotFoundException; {:try_start_1 .. :try_end_1} :catch_2
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_1

    .line 54
    nop

    .end local v6    # "file":Ljava/io/File;
    .end local v7    # "filereader":Ljava/io/FileReader;
    .end local v8    # "bufReader":Ljava/io/BufferedReader;
    .end local v9    # "line":Ljava/lang/String;
    goto :goto_1

    .line 52
    :catch_1
    move-exception v5

    .line 53
    .local v5, "e":Ljava/io/IOException;
    invoke-virtual {v5}, Ljava/io/IOException;->printStackTrace()V

    goto :goto_1

    .line 50
    .end local v5    # "e":Ljava/io/IOException;
    :catch_2
    move-exception v5

    .line 51
    .local v5, "e":Ljava/io/FileNotFoundException;
    sget-object v6, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v6, v5}, Ljava/io/PrintStream;->println(Ljava/lang/Object;)V

    .line 54
    .end local v5    # "e":Ljava/io/FileNotFoundException;
    nop

    .line 56
    :goto_1
    return v4
.end method
