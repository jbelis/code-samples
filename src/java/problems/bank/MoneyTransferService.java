package bank;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import org.apache.log4j.Logger;
import java.sql.SQLException;

private static class AccountTransaction {
}

public class MoneyTransferService {
	public void transferFunds(Account source, Account target, BigDecimal amount, boolean allowDuplicateTxn) throws IllegalArgumentException, RuntimeException {
Connection conn = null;
try {
conn = DBUtils.getConnection();
PreparedStatement pstmt = conn.prepareStatement("Select * from accounts where acno = ?");
pstmt.setString(1, source.getAcno());
ResultSet rs = pstmt.executeQuery();
Account sourceAccount = null;
if(rs.next()) {
sourceAccount = new Account();
//populate account properties from ResultSet
}
if(sourceAccount == null){
throw new IllegalArgumentException("Invalid Source ACNO");
}
Account targetAccount = null;
pstmt.setString(1, target.getAcno());
rs = pstmt.executeQuery();
if(rs.next()) {
targetAccount = new Account();
//populate account properties from ResultSet
}
if(targetAccount == null){
throw new IllegalArgumentException("Invalid Target ACNO");
}
if(!sourceAccount.isOverdraftAllowed()) {
if((sourceAccount.getBalance() - amount) < 0) {
throw new RuntimeException("Insufficient Balance");
}
}
else {
if(((sourceAccount.getBalance()+sourceAccount.getOverdraftLimit()) - amount) < 0) {
throw new RuntimeException("Insufficient Balance, Exceeding Overdraft Limit");
}
}
AccountTransaction lastTxn = .. ; //JDBC code to obtain last transaction of sourceAccount
if(lastTxn != null) {
if(lastTxn.getTargetAcno().equals(targetAccount.getAcno()) && lastTxn.getAmount() == amount && !allowDuplicateTxn) {
throw new RuntimeException("Duplicate transaction exception");//ask for confirmation and proceed
}
}
sourceAccount.debit(amount);
targetAccount.credit(amount);
TransactionService.saveTransaction(source, target,  amount);
}
catch(Exception e){
logger.error("",e);
}
finally {
try { 
conn.close(); 
} 
catch(Exception e){ 
//Not everything is in your control..sometimes we have to believe in GOD/JamesGosling and proceed
}
}
}
}